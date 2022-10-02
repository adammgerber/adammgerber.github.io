import spacy
import icu


# with open('top50words.txt', 'r')as f:
#     doc = f.read().replace('\n', '')

# word_list = [x for x in doc]
# twentykay = []

# for i in word_list:
#     while word_list.index(i) < 20000:
#         twentykay.append(i)

# print(twentykay)


with open('top50words.txt', 'r')as f:
    doc = f.read().replace('\n', '')

nlp = spacy.load('ru_core_news_md')
doc = nlp(doc)

verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
nouns = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
adjs = [token.lemma_ for token in doc if token.pos_ == 'ADJ']


collator = icu.Collator.createInstance(icu.Locale('ru_RU.UTF-8'))
sorted_verbs = sorted(verbs,key=collator.getSortKey)
sorted_nouns = sorted(nouns,key=collator.getSortKey)
sorted_adjs = sorted(adjs,key=collator.getSortKey)


final_verbs = list(dict.fromkeys(sorted_verbs))
final_nouns = list(dict.fromkeys(sorted_nouns))
final_adjs = list(dict.fromkeys(sorted_adjs))
final_words = final_adjs + final_nouns + final_verbs

final_words_50k = list(dict.fromkeys(final_words))

words_20k = []

for i in final_words_50k:
    if final_words_50k.index(i) < 20000 and len(i) > 2:
        words_20k.append(i)

words = str(words_20k)

with open('top20words.txt', 'w')as f:
    f.write(words)
