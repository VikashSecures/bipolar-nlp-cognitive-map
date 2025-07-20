import requests
import http,json
import openai 
import os
import pandas as pd
from datetime import datetime
from GPTCall import ask_chatgpt 
from SaveExcel import update_sheet_preserving_format


def keyfunction_readme():
    i=i
    # key function steps 
    #-------------------------------------

    # 1.  In mypath folder, there is an excel file called Cognitive Map Graph Processing v3 2024.02.14.xlsx
    # 2.  The excel file has three sheets: articles, paragraphs, and sentences  
        # Sheet name: paragraphs
        #Columns: ['ID', 'Paragraph text', 'url', 'category labels', 'summarised key points in simple sentences', 'processing user', 'processing date']

        #Sheet name: sentences
        #Columns: ['ID', 'paragraph ID', 'CMG Auto with GPT', 'CMG by Human Expert', 'Justification of the correction', 'processing user', 'processing date', 'correction user', 'corrction date']

    # 3. Read the articles to a dataframe called df_article, run through it row by row, call ChatGPT API, 
    #     if the row processed is not yes, then, ask gpt to group it into major paragraphs and sub pagragphs, add to paragraph df
    #      #Columns: Article ID	Full text	url	category labels	processed	processing user	processing date

def main():
    print ("main function started \n--------------------")
    mypath = 'G:/NMIT/research project a/CODE/'
    myexcelfile=mypath+'7_Cognitive_Map_Graph_Processing.xlsx'    
    
    #check_excelfile_info(myexcelfile) # print sheet heads
    
    df_paragraphs = pd.read_excel(myexcelfile, sheet_name='paragraphs')
    df_articles = pd.read_excel(myexcelfile, sheet_name='articles')

    row_start=0;    row_end=0 # end is 0 means to the end 
    df_paragraphs, df_articles=group_paragraphs(df_paragraphs,  df_articles, row_start, row_end)
    
    update_sheet_preserving_format(myexcelfile, 'paragraphs', df_paragraphs)
    update_sheet_preserving_format(myexcelfile, 'articles', df_articles)


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

def testjson():
    jsonstr="""json {
        "article_label": "Pressure Injuries Overview",
        "paragraphs": [
            {
            "label": "Definition and Causes of Pressure Injuries, Risk Factors for Pressure Injuries",
            "original text": "......"
            },

            {
            "label": "test 4",
            "original text": "......"
            },

        
            {
            "label": "test 3",
            "original text": "....

        """
    return jsonstr

def group_paragraphs_prompt():      
    #specific prompt
    myprompt3=\
    """ 
    1) Read the following article content thoroughly and segment it into structured paragraphs specifically related to the knowledge of bipolar disorder.
    2) Assign detailed and meaningful labels to each paragraph that reflect key concepts relevant to bipolar disorder, such as symptoms, treatments, triggers, patient outcomes, and any other important clinical aspects.
    3) Include subparagraphs with their own labels to provide a hierarchical structure within the content where necessary, particularly for complex descriptions or discussions involving multiple factors.
    4) When labeling subparagraphs, ensure to combine the main paragraph label with a comma before it, e.g., "Symptoms and Signs of Bipolar Disorder, Prolonged Grief Disorder."
    5) Use quoted strings for labels and separate different labels with commas. Labels should be comprehensive enough to facilitate understanding without additional context.
    6) Construct the output in JSON format with the following structure:
       {"article_label": "Overall Topic Summary", "paragraphs": [{"label": "Subtopic Label", "original text": "Detailed Paragraph Content"}, ...]} 
    7) If the article's content is extensive and could exceed character limits, divide it into coherent subparts, assigning new, unique labels that continue to reflect the content accurately.
    8) Exclude references, citations, or any ancillary sections that do not provide substantive content about bipolar disorder. However, include sections with summaries or discussions crucial for understanding the disorder.
    9) Ensure that the JSON is complete and properly closed. If the full content cannot be processed in one go due to length, indicate continuation in subsequent JSON structures.
    10) Only provide the structured JSON output in your response. My program will parse the JSON to extract and utilize the information.
    11) Maintain the same language and clinical terms relevant to bipolar disorder to preserve the content's integrity and accuracy.
    12) If a section contains detailed lists, such as diagnostic criteria or types of treatments, combine list items by comma and add them as a single sentence under the same label.
    13) Aim to capture all key sections typically found in articles related to bipolar disorder, such as Introduction, Background, Symptoms, Treatments, Triggers, Patient Outcomes, and any other relevant headings specific to the article.
    14) Ensure to capture all major topics related to bipolar disorder until the end of the article.

    Here is the article content: 
    """
# other prompt
    '''*myprompt3 = \
        """ 

    1) Read the following article content thoroughly and segment it into structured paragraphs. 
    2) Assign detailed and meaningful labels to each paragraph that encapsulate the core topic and information contained within. Ensure that these labels are clear and specific to the paragraph's content.
    3) Include subparagraphs with their own labels to provide a hierarchical structure within the content where necessary, especially for articles with complex topics or multiple subtopics.
    4)when adding label for subparagraph make sure to combine the main paragraph label with a comma before it as "Symptoms and Signs of Depressive Disorders,Prolonged grief disorder'

    5) Use quoted strings for labels and separate different labels with commas. Labels should be comprehensive enough to facilitate independent processing and understanding without additional context.
    6) Construct the output in JSON format with the following structure:
       {"article_label": "Overall Topic Summary", "paragraphs": [{"label": "Subtopic Label", "original text": "Detailed Paragraph Content"}, ...]} 
    7) If the article's content is extensive and could exceed character limits, divide it into coherent subparts, assigning new, unique labels that continue to reflect the content accurately.
    8) Exclude references, citations or any ancillary sections that do not provide substantive content. However, if these references include summaries or discussions that are important for understanding, include them under same label.
     9) Ensure that the JSON is complete and properly closed. If the full content cannot be processed in one go due to length, indicate the continuation in subsequent JSON structures.
     10) Only provide the structured JSON output in your response. My program will parse the JSON to extract and utilize the information.
    11) Ensure that the JSON output maintains the same language and technical terms as the original article to preserve the content's integrity and accuracy.

     12) If a section contains detailed lists, such as diagnostics criteria or types of treatements, combine the list items by comma as add them as a single sentence to the same label.                
    13) Aim to capture all key sections typically found in articles of the subject matter, such as Introduction, Background, Methods, Results, Discussion, Conclusion, and any other relevant headers or titles specific to the article.
    14) Ensure to capture all major topics till the end of the article.






            Here is the article content: """
            '''
    return myprompt3 
#13)If a section contains detailed lists, such as diagnostic criteria or types of treatments, combine two of the list items by commas and add them as a single sentences to same label category.

def group_paragraphs(df_paragraphs,  df_articles, row_start, row_end):
    print("\n group_paragraphs function \n --------------------------------------")
    myprompt=group_paragraphs_prompt()    

    """
    response_text = testjson()
    print(response_text)
    article_id=5
    df_paragraphs, article_label=parse_paragraphs_json(response_text,article_id,df_paragraphs)
    print(article_label)
    """

    if row_end == 0:   row_end = df_articles.index[-1]
    for index in range(row_start, row_end + 1):
        if index > df_articles.index[-1]:  # Check to ensure index is within DataFrame bounds
            break  # Exit the loop if index exceeds the number of rows in the DataFrame

        # Access row by index
        row = df_articles.iloc[index]
        article_id=row['Article ID']
        fulltext = str(row['Full text'])
        processed_flag = row['processed']
        #askgptcontent=myprompt+fulltext


        # Proceed if processed is not 'yes' and fulltext is not empty 
        if processed_flag!='Yes'and fulltext and fulltext.lower() != 'nan':            
            response_text = ask_chatgpt(myprompt, fulltext)
            print("-------response_text-----------------------")
            print(response_text)

            # Update the DataFrame with the response
            df_paragraphs, article_label=parse_paragraphs_json(response_text,article_id,df_paragraphs) 
            df_articles.loc[index, 'processed'] = 'Yes'
            df_articles.loc[index, 'category labels'] = article_label
            df_articles.loc[index, 'json str'] = response_text
        
    return df_paragraphs,df_articles

import re


def find_complete_pairs(json_str):
    match = re.search(r'"article_label":\s*"(.*?)"', json_str)  # the returned string may not have a complete json structure; use re to find the related components
    if match:  summary_label = match.group(1)        
    else:      summary_label ="Summary label not found."

    pattern = r'\{\s*"label"\s*:\s*(?:\[.*?\]|".*?")\s*,\s*"original text"\s*:\s*".*?"\s*\}'
    matches = re.findall(pattern, json_str, re.DOTALL)
    print("here are found maches strings: \n---------------------\n", matches)
    # Attempt to parse each match as JSON directly into dictionaries
    complete_pairs = []
    for match in matches:
        try:
            # Each match is expected to be a valid JSON string
            pair_dict = json.loads(match)
            complete_pairs.append(pair_dict)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from match: {e}")
    
    return complete_pairs, summary_label

def parse_paragraphs_json(response_text, article_id, df_paragraphs):
    completed_pairs, article_label = find_complete_pairs(response_text)

    #print("Found total ", len(completed_pairs), "completed paragraphs in json string.")
    #print ("completed pairs are: ", completed_pairs)
    if df_paragraphs.empty:   last_id = 0
    else:                     last_id = df_paragraphs['ID'].max()
    
    for paragraph in completed_pairs:  # Now 'paragraph' is already a dictionary
        if isinstance(paragraph, dict):
            label = paragraph.get("label", "")
            original_text = paragraph.get("original text", "")
            # Continue processing
        else:
            label = "Unexpected data format error"
            original_text = paragraph
           
        last_id += 1
        new_row = pd.DataFrame({
            'ID': [last_id], 
            'Article ID': [article_id],
            'category labels': [label],
            'Paragraph text': [original_text]
        })
        df_paragraphs = pd.concat([df_paragraphs, new_row], ignore_index=True)
    
    return df_paragraphs, article_label




main()