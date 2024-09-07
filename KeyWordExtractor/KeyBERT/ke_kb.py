#Not applying any preprocessing steps 
#May Have to do that first tho O.O


from keybert import KeyBERT
import pandas as pd


filename = "Data.csv"
raw = pd.read_csv(filename)

print(type(raw.iloc[0,1]))

kw_model = KeyBERT()

result_data = {'name': [], 'keywords':[]}
for i in range(len(raw.axes[0])):
    print(f"Running keyword extraction for ",raw.iloc[i,0])
    doc = raw.iloc[i,1]
    keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2))
    result_data['keywords'].append(keywords)
    result_data['name'].append(raw.iloc[i,0])
    print("Done! Saving Keywords")
df = pd.DataFrame(result_data, index=None)
print("Saving results to file --> out.csv")
df.to_excel('out.xlsx', index=False)
