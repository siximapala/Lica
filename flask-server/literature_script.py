import fitz
import re
# Импортируем необходимые компоненты для извлечения сущностей из текста
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc
)

def wrap(names):
    """
    Форматирует список имён в формат "Фамилия И.О." для списка литературы
    """
    res = []
    for i in names:
        if '.' in i:
            n = i.replace('.', ' ')
            n = i.split(' ')
            if len(n) == 1:
                n = i.split('.')
                if len(n) > 1:
                    i = f"{n[-1]}, {n[0][0]}. {n[1][0]}."
                else:
                    i = f"{n[0][0]}"
            elif len(n) == 2:
                fam = n[-1].lower()
                fam = fam[0].upper() + fam[1:]
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

def get_text_from_pdf(file1):
    """
    Извлекает текст из PDF-файла с помощью PyMuPDF (fitz)
    """
    text = ''
    with fitz.open(file1) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    text = text.replace("  ", " ")
    return text.replace("\n", " ")

def extract_uppercase_russian_phrase(text):
    """
    Ищет заглавные русские фразы (обычно название статьи)
    """
    matches = re.findall(r'\b(?:[А-ЯЁ]{1,}[^\w.\n]?\s*){2,}\b', text)
    if len(matches) > 1 and len(matches[1]) > 5:
        return matches[0].strip().replace("\n", "") + ' ' + matches[1].strip().replace("\n", "")
    return matches[0].strip().replace("\n", "")

def extract_dict_of_names(text):
    """
    Извлекает имена авторов из текста с помощью Natasha
    """
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
        for i in list(names_dict.keys())[:2]:
            res.append(i)
        return wrap(res)
    return None

def get_doi(text):
    """
    Пытается найти DOI в тексте
    """
    try:
        index = text.index("doi")
        doi = text[index:index + 28]
        return doi.replace("doi: ", "")
    except ValueError:
        return "0"

def get_date(text):
    """
    Пытается найти год публикации в тексте
    """
    get_date = re.search(r'[^-]\d{4}[^-]', text[-1000:])
    if get_date:
        return re.search(r'\d{4}',get_date.group()).group()
    else:
        get_date = re.search(r'[^-]\d{4}[^-]', text[:1000])
        if get_date:
            return re.search(r'\d{4}',get_date.group()).group()
    return "0"

def get_title(text):
    """
    Извлекает название статьи из текста
    """
    title1 = extract_uppercase_russian_phrase(text).lower()
    title2 = "-1"
    if (title2 == "-1"):
        title = title1[0].upper() + title1[1:]
    else:
        title = title2[0].upper() + title2[1:]
        title = re.sub(r'[^a-zA-Z0-9а-яА-Я\s]', '', title)
    return title

def make_string(title, authors, doi, date):
    """
    Формирует строку для списка литературы из данных о статье
    """
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
    """
    Извлекает всю нужную информацию из одного PDF-файла
    """
    text = get_text_from_pdf(file)
    title = get_title(text)
    names = extract_dict_of_names(text)
    doi = get_doi(text)
    if (doi == "0" or doi == "-1"):
        doi = "-1"
    date = get_date(text)
    return make_string(title, names, doi, date)

def get_all(files):
    """
    Обрабатывает список файлов и возвращает отсортированный список литературы
    """
    if files == [] or files == [""]:
        print("Error file")
        return
    result = []
    for f in files:
        result.append(get_info_of_text(f))
    result = sorted(result)
    string = ""
    n = 1
    for i in result:
        string = string + f"{n}. {i} \n"
        n += 1
    return string