import requests
import http,json
import os
import pandas as pd
from datetime import datetime
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
    
    df_paragraphs = pd.read_excel(myexcelfile, sheet_name='paragraphs')
    df_sentences = pd.read_excel(myexcelfile, sheet_name='sentences')

    row_start=0;    row_end=0 # end is 0 means to the end 
    df_paragraphs, df_sentences=summarise_keypoints(df_paragraphs,  df_sentences, row_start, row_end, myexcelfile)


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

def summarise_prompt():
    #specific prompt
    myprompt1=\
    """Summarise the key points and knowledge specifically related to bipolar disorder in the following paragraph.
        1) Focus on identifying critical elements such as symptoms, treatments, triggers, patient outcomes, and any clinical aspects relevant to bipolar disorder.
        2) Use bullet points to clearly delineate each key insight or piece of actionable information.
        3) Avoid background details or general explanations; concentrate on direct insights that contribute to the understanding of bipolar disorder.
        4) Use specific names and nouns instead of pronouns to ensure clarity for independent processing of each point.
        5) Each sentence should be self-contained and avoid referencing earlier sentences. Maintain the original language and clinical terminology used in the text.
        6) If a sentence in the paragraph is already concise and specific, you may use it as is.
        7) Use the same language as the paragraph content to preserve the clinical relevance.
    
        Here is the paragraph: """

    #other prompt
    '''
    myprompt1=\
    """Summarise the following paragraph key points and knowledge points. 
        1) Craft the summary using bullet points to clearly delineate each key insight or piece of actionable information. 
        2) Avoid explanations and background details; focus mainly on direct insights and actions that can be derived from the text.
        3) Use specific names and nouns instead of pronouns to ensure clarity for independent processing of each point.
 
        4) Do not use pronouns. Use the proper nouns because the sentences will be further processed individually. 
        5) Each sentence is one line. Each sentence will be processed independently. So try to keep the meaning of the sentence self-contained.
        6) If the original sentence is already a simple sentence, you can use the same sentence.
        7) Use the same language as the paragraph content.
    
        Here is the pragraph: """
    '''
      
    return myprompt1

def summarise_keypoints(df, df_sentences,row_start, row_end, myexcelfile):
    print("\n summarise_keypoints function \n --------------------------------------")
    myprompt=summarise_prompt()
    
    if row_end == 0:   row_end = df.index[-1]
    for index in range(row_start, row_end + 1):
        if index > df.index[-1]:  # Check to ensure index is within DataFrame bounds
            break  # Exit the loop if index exceeds the number of rows in the DataFrame

        # Access row by index
        row = df.iloc[index]
        mycontent = row['Paragraph text']
        summary = row['summarised key points in simple sentences']
        processedflag=row['processed']

        # Proceed if 'Paragraph text' is not empty and processed is not 'Yes' 
        if processedflag!='Yes' and pd.notna(mycontent)  and mycontent.strip():
            response_text = ask_chatgpt(myprompt, mycontent)
            print("-------response_text-----------------------")
            print(response_text)

            # Update the DataFrame with the response
            df.at[index, 'summarised key points in simple sentences'] = response_text
            paragraph=response_text
            df_sentences=write_summarisedPoints_to_sentence_rows(paragraph,index, df_sentences)
            df.at[index,'processed']='Yes'
            if(index%10 == 0):
                try: 
                    update_sheet_preserving_format(myexcelfile, 'paragraphs', df)
                    update_sheet_preserving_format(myexcelfile, 'sentences', df_sentences)
                except:
                    print("An exception occurred, saving problems")

    try: 
        update_sheet_preserving_format(myexcelfile, 'paragraphs', df)
        update_sheet_preserving_format(myexcelfile, 'sentences', df_sentences)
    except:
        print("An exception occurred, saving problems")
    return df,df_sentences


def write_summarisedPoints_to_sentence_rows(paragraph,index, df_sentences):
    print ("\n split_sentences function index=",index," \n -------------------------------------")
    
    if not df_sentences.empty:
        # If df_sentences is not empty, continue IDs from the last used ID
        sentence_id = df_sentences['Sentence ID'].max() + 1
    else:  sentence_id = 1  # If df_sentences is empty, start IDs from 1

    new_rows = []  # Initialize a list to hold new rows
    paragraph_id = index  
    summarised_sentences = paragraph.split('\n')
        
    for sentence in summarised_sentences:
            #print("\n here=", sentence)
            if sentence and sentence.strip():  # Check if the sentence is not just whitespace
                # Create a new row with existing columns, setting default values for unspecified columns
                new_row = {col: '' for col in df_sentences.columns}  # Initialize all columns to default values
                new_row.update({
                    'Sentence ID': sentence_id, 
                    'Paragraph ID': paragraph_id+1, 
                    'Sentence text': sentence.strip()
                })
                new_rows.append(new_row)
                sentence_id += 1

    # Append new rows to df_sentences DataFrame
    if new_rows:
        df_sentences = pd.concat([df_sentences, pd.DataFrame(new_rows)], ignore_index=True)
    
    return df_sentences
    
main()
