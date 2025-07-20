import requests
import http,json
import openai 
import os
import pandas as pd
from datetime import datetime, time
import time
from GPTCall import ask_chatgpt
from SaveExcel import update_sheet_preserving_format

def keyfunction_readme():
    i=i
    # key function steps 
    #-------------------------------------

    # 1.  In mypath folder, there is an excel file called Cognitive Map Graph Processing v3 2024.02.14.xlsx
    # 2.  The excel file hastwo sheets, one are paragraphs, and one are cognitive map graph sentences 
        # Sheet name: paragraphs
        #Columns: ['ID', 'Paragraph text', 'url', 'category labels', 'summarised key points in simple sentences', 'processing user', 'processing date']

        #Sheet name: sentences
        #Columns: ['ID', 'paragraph ID', 'CMG Auto with GPT', 'CMG by Human Expert', 'Justification of the correction', 'processing user', 'processing date', 'correction user', 'corrction date']

    # 3. Read the original text to a dataframe called df, run through it row by row, call ChatGPT API, 
    #     use the following myprompt to summarise the key points of the text:
    #     myprompt="1) Summarise the key point, or information/knowledge, of the following text,  
    #               2) use simple structrued setnecnes;  3) each sentence should be self contained, avoid using propositions 
    #               to refer to entities in ealrier sentences; 4) response in format of  Key Points =  'the key points' " 
    # 4. Parse the ChatGPT response to extract the keypoints, and update the keypoints in col4 of the dataframe df 
    # 5. For each row in col4, ask chatGPT API to convert the sentences into  head, relation, tail structure. For example, 
    #        Acute kidney injury is a rapid decrease in renal function over days to weeks. will be separated into: 
    #        Acute kidney injury, is, a rapid decrease in renal function (duration: over days to weeks).  
    #     Here we use () to enclose properties of the head, tail or relation. Multiple properties can be separated with comma. 
    # 6. Note that a sentence may not have a tail, which can be represented with a -. For example, 
    #       Acute kidney injury can be fatal.   can be converted as
    #       Acute kidney injury, can be fatal, -. 
    # 7. For a sentence with a sub clause, use [] to enclose the main sentence and the sub clause. Use []-(connecting word)-[]. for the converted sentence. 
    #      for example,  Tom had AKI when he was 50.  will be converted as 
    #                   [Tom, had AKI, -]-(when)-[Tom, was 50, -]
    #      note the relationship needs to be meaningful. is, have, get are too short to represent the meaning of the relation. 
    # 8. Resonse will be in format of  FCM scripts= ' ****' 
    # 9. Extract FCM scripts from the response, and write to col5 of df

def main():
    print ("main function started \n--------------------")
    time_started=time.time()

    mypath = 'G:/NMIT/research project a/CODE/'
    myexcelfile=mypath+'7_Cognitive_Map_Graph_Processing.xlsx'      
    #check_excelfile_info(myexcelfile)
    
    df_sentences = pd.read_excel(myexcelfile, sheet_name='sentences')
    row_start=0;       row_end=0 # end is 0 means to the end 
    convertsentence_toCMG(df_sentences,row_start, row_end, myexcelfile)

    

    time_finished=time.time()
    timeused=time_finished-time_started
    print("Time used=", timeused)


def check_excelfile_info(myexcelfile):
# check the sheet names and columns in the excel file
     # Iterate through all sheets
    print(myexcelfile)
    xls = pd.ExcelFile(myexcelfile)

    for sheet_name in xls.sheet_names:
        # Read each sheet
        df = pd.read_excel(xls, sheet_name)
        
        # Print the sheet name and its columns
        print(f"Sheet name: {sheet_name}")
        print("Columns:", df.columns.tolist())

def convertCMG_prompt():
    #specific prompt
    myprompt="""Convert the following sentence, related to bipolar disorder, into a head, relation, tail structure.
        1) Ensure the head represents the main entity (e.g., a symptom, patient, or treatment).
        2) The relation should capture the key action, condition, or state relevant to bipolar disorder.
        3) The tail should provide additional context or details, such as the duration, intensity, or specific characteristics of the head-relation pair.
        
        Example:
        Original: "Patients with bipolar disorder often experience intense mood swings."
        Head: Patients with bipolar disorder
        Relation: experience
        Tail: intense mood swings.
        
        4) Respond only in the specified head, relation, and tail format without further explanation.
        5) Maintain the original clinical language and terminology used in the sentence.
        6) For sentences containing multiple pieces of information, ensure the relation accurately captures the main action or state, while the tail provides necessary qualifiers or details to preserve the sentence's original meaning.
        7) If the sentence includes specific treatments, symptoms, or patient outcomes, ensure that these elements are clearly identified in the head or tail to maintain clinical relevance.
    """

    #other prompt
    '''
    myprompt=""" Convert the sentence into  head, relation, tail structure. 
        1)Provide only the head, relation, and tail structure without any explanation.

        Example:
        Head: John
        Relation: runs
        Tail: very fast.
        
        2)Respond only according to the structure requested.
        
        3)Sometimes the relation or tail includes phrases, not just single nouns or verbs. For example:
        
        "Weak Mary has to breathe over 30 times in a minute." should be converted to:
        Head: Weak Mary
        Relation: has to breathe
        Tail: over 30 times in a minute.
        In this case, the tail describes the relation further. Similarly, "John runs very fast." should be:
        Head: John
        Relation: runs
        Tail: very fast.
        
        4)Maintain the original language of the sentence in your response.
        
        5)If a sentence contains multiple pieces of information, ensure that the relation captures the action or state accurately, and the tail provides the necessary detail or qualifier without breaking the inherent meaning.
        
        6)For complex sentences where the tail modifies the relation, include these modifiers within the tail to maintain the sentence's original context and meaning. 
                        """
    '''
    return myprompt

def convertsentence_toCMG(df_sentences,row_start, row_end ,myexcelfile):
    print ("convertsentence_toCMG function started \n--------------------")
    myprompt=convertCMG_prompt()
    if row_end == 0:   row_end = df_sentences.index[-1]

    for index in range(row_start, row_end + 1):  # +1 because the range end is exclusive
        if index < len(df_sentences) : # Check to ensure index is within DataFrame bounds
            if df_sentences.at[index, 'processed'] !='Yes': 
                sentence_text = df_sentences.at[index, 'Sentence text']
                response_text = ask_chatgpt(myprompt, sentence_text)
                df_sentences.at[index, 'CMG Auto with GPT'] = response_text
                df_sentences.at[index, 'processed'] = 'Yes'
                
                if(index%10 == 0):
                    try: 
                        update_sheet_preserving_format(myexcelfile, 'sentences', df_sentences)
                    except:
                        print("An exception occurred, saving problems")
        else:
            break  
    update_sheet_preserving_format(myexcelfile, 'sentences', df_sentences)
    return df_sentences
  
main()
