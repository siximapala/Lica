import fitz
import openai
import re
import time
import PyPDF2
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    LOC,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,
    Doc)

openai.api_key = "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"#"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"
model_engine = "davinci-002"
max_tokens = 100


#def find_substring_name(text, substring):
    #annotation_index = text.find("Аннотация")
    #annotation_index2 = text.find("ABSTRACT")
    #if annotation_index != -1 or text.find(substring) < annotation_index or annotation_index2 != -1 or text.find(substring) < annotation_index2:
        #return True



def get_answer_from_gpt(prompt, t = None):
    #print(prompt[:50])
    if (t == None):
        t = 0.05
    try:
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=t,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer_from_gpt = completion.choices[0].text.splitlines()
        #print(answer_from_gpt[-1])
    except Exception as e:
        #print(e)
        return "-1"
    return answer_from_gpt[-1]

def wrap(names):
    res = []
    for i in names:
        if '.' in i:
            
            n = i.replace('.', ' ')
            n = i.split(' ')
            #print(n)

            if len(n) == 1:
                n = i.split('.')
                if len(n) > 1:
                    i = f"{n[-1]}, {n[0][0]}. {n[1][0]}."
                else:
                    i = f"{n[0][0]}"
            elif len(n) == 2:
                fam = n[-1].lower()
                fam = fam[0].upper() + fam[1:]
                #print(fam)
                i = f"{fam}, {n[0]}"
            else:
                i = f"{n[-1]}, {n[0]} {n[1]}"
            res.append(i)
            continue
        splitted_names = i.split()
        if len(splitted_names) == 2:
            fam = splitted_names[0].lower()
            fam = fam[0].upper() + fam[1:]
            name = splitted_names[1]
            res.append(f"{fam}, {name[0][0]}.")
        if len(splitted_names) == 3:
            fam = splitted_names[0].lower()
            fam = fam[0].upper() + fam[1:]
            name = splitted_names[1]
            ot = splitted_names[2]
            res.append(f"{fam}, {name[0][0]}. {ot[0][0]}.")
    return res



def extract_authors(text):
    authors = get_answer_from_gpt("Выдели из текста не повторяющиеся фамилии имена и отчества только людей и верни их ФИО через запятую в формате \"Фамилия И.О.\":" + text[:1000], 0.7).split(',')
    #print(authors)
    if (authors == "-1"):
        return "-1"
    return wrap(authors)


def get_text_from_pdf(file1):
    text = ''
    with fitz.open(file1) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    #print(text)
    text = text.replace("  ", " ")
    return text.replace("\n", " ")
    '''doc = fitz.open(file) 
    text = "" 
    for page in doc: 
        text += page.get_text()
    return text'''


def extract_uppercase_russian_phrase(text):

    matches = re.findall(r'\b(?:[А-ЯЁ]{1,}[^\w.\n]?\s*){2,}\b', text)
    #print(matches)
    if len(matches[1]) > 5:
        return matches[0].strip().replace("\n", "") + ' ' + matches[1].strip().replace("\n", "")
    return matches[0].strip().replace("\n", "")



def extract_dict_of_names(text):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)
    
    doc = Doc(text)
    doc.segment(segmenter) 
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)
    
    names_dict = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}
    if names_dict:
        res = []
        #print(names_dict.keys())
        for i in list(names_dict.keys())[:2]:
            #if find_substring_name(text, i):
            res.append(i)
        return wrap(res)
    return None



def get_doi(text):
    try:
        index = text.index("doi")
        
        doi = text[index:index + 28]
        return doi.replace("doi: ", "")
    except ValueError:
        
        #gpt = get_answer_from_gpt("Верни только численное представление doi данного текста, если не удалось, верни 0 " + text[:2500], 0.01)
        #if gpt != "0" and gpt != "-1":
            #return gpt
        return "0"
    

def get_date(text):
    get_date = re.search(r'[^-]\d{4}[^-]', text[-1000:])
    if get_date:
        return re.search(r'\d{4}',get_date.group()).group()
    else:
        get_date = re.search(r'[^-]\d{4}[^-]', text[:1000])
        if get_date:
            return re.search(r'\d{4}',get_date.group()).group()
    return "0"
    #return get_answer_from_gpt("Верни только дату публикации или написания данного текста в формате день.месяц.год, если найти не удалось верни 0: " + text[:2000], 0.5)



def get_title(text):
    title1 = extract_uppercase_russian_phrase(text).lower()
    #title2 = get_answer_from_gpt("Верни только название данного текста без лишних слов, если не удастся верни -1: " + text[:1000], 0.2).lower()
    title2 = "-1"
    if (title2 == "-1"):
        title = title1[0].upper() + title1[1:]
    else:
        title = title2[0].upper() + title2[1:]
        title = re.sub(r'[^a-zA-Z0-9а-яА-Я\s]', '', title)
        #title = title.replace("название", "")
    #title2 = title2.replace("текста", "").lstrip()
    return title

'''
#Работа с текстом
file =  'C:/Users/kopte/Downloads/90.Raxmatova+Gavharoy+Muxamadali+qizi_Rus_163_51.pdf'#"C:/Users/kopte/Downloads/mbb283.pdf"
text = get_text_from_pdf(file)

#Находим название
title = get_title(text)
print("title: " + title )

#Находим авторов
names = extract_dict_of_names(text)
authors = extract_authors(text, names)
if authors == "-1":
    authors = names
print(authors)

#Находим doi
doi = get_doi(text)
if (doi == "0" or doi == "-1"):
    doi = "-1"
print("doi: " + doi)


#Находим дату
date = get_date(text)
print(date)


string = f"{authors[0]} {title} / "
for i in range(len(authors)):
    string = string + authors[i] + " "
string = string + " - DOI: " + doi 
string = string + " -" + date


print(string)
'''
def make_string(title, authors, doi, date):
    string = f"{authors[0]} {title} / "
    for i in range(len(authors)):
        string = string + authors[i] + " "
    if doi != "-1" and doi != "0":
        string = string + " - DOI: " + doi 
    if date != "0" and date != "-1" and not(date is None):
        string = string + " - " + date
    string = string.replace("  ", " ")
    return string.replace('\n', '')

def get_info_of_text(file):
    text = get_text_from_pdf(file)
    title = get_title(text)
    names = extract_dict_of_names(text)
    #print(names)
    #authors = extract_authors(text) 
    #authors = names
    #print(authors)
    #if authors == "-1" or authors == []:
        #authors = names
    doi = get_doi(text)
    if (doi == "0" or doi == "-1"):
        doi = "-1"
    date = get_date(text)
    return make_string(title, names, doi, date)




def get_all(files):
    #----------------------------------------------------------------------------------------------------------------------------
    #начало мейна

    #Читаем ссылки на файлы из которых будем формировать список литературы
    #обязательно pdf
    if files == [] or files == [""]:
        print("Error file")
        return
        #files = ["C:/Users/kopte/Downloads/90.Raxmatova+Gavharoy+Muxamadali+qizi_Rus_163_51.pdf", "C:/Users/kopte/Downloads/mbb283.pdf", "C:/Users/kopte/Downloads/CAJAR+0106.pdf", "C:/Users/kopte/Downloads/766846.pdf", "C:/Users/kopte/Downloads/403_30_i.pdf"]

    #читаем ссылку на файл куда будем записывать результат
    #write_file = input()
    #if write_file == "":
        #write_file = "result.txt"

    #формирование списка итоговых строки, содержащих список литературы
    result = []
    for f in files:
        result.append(get_info_of_text(f))
        #print(get_text_from_pdf(f))
        #print("---------------------------------------------------------------------------------")
    result = sorted(result)
    string = ""
    n = 1
    for i in result:
        string = string + f"{n}. {i} \n"
        n += 1
    
    #вывод результата
    #print(string)
    return string
    #with open(write_file, "w") as file:
        #n = 1
        #for i in result:
            #i = f"{n}. {i}"
            #file.write(i)
            #file.write('\n')
            #n += 1
