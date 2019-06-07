import pandas as pd
import json

header = ["id", "activity", "data","gender", "salary"]


df = pd.read_csv('chicago.csv', quotechar='"', sep=',', encoding='utf-8-sig', names=header)


print (df.head())
print (df.columns)

print (df.shape)


# Isolate the columns case_id and activity_id
s = df.loc[:,['id', 'activity']]



# Force the column to be of type string (otherwise the concatenation does not work)
s['activity'] = s['activity'].astype(str)
s['id'] = s['id'].astype(str)

# For each traces, concatenate the activity; e.g., 1=>1-2-1, 2=>1-3-3-3-4-1, 3=>1-2-1
s = s.groupby('id')['activity'].apply(lambda x: "-------".join(x)).to_frame()


s['id'] = pd.Series(s.index, index=s.index)
seqs = s.activity.str.split("-------").tolist()

j = {}
j["depth"] = "1"
j["Journeys"] = {}
count = 0
seqs = [['All other home activities','Work/Job','All other home activities','Work/Job','All other home activities'],['All other home activities','Work/Job','All other home activities'],['All other home activities','Shopping','Shopping','All other home activities']]

for i, seq in enumerate(seqs):
    if seq[0] != 'All other home activities' or seq[-1] != 'All other home activities':
        continue
    count+=1
    if count > int(1237/2):
        continue
    i_str = str(i)

    j["Journeys"][i_str] = {}
    j["Journeys"][i_str]["count_pattern"] = "6"
    j["Journeys"][i_str]["count_journey"] = "6"
    j["Journeys"][i_str]["type"] = "representative"
    j["Journeys"][i_str]["events"] = []
    for a in seq:
        j["Journeys"][i_str]["events"].append({"trip_main_purpose":a})


f = open('static-response.json',"w", encoding='utf-8')
j = json.dumps(j, ensure_ascii=False)
f.write(str(j))



'''
{
   "depth":"0",
   "Journeys":{
      "1":{
         "count_pattern":"6",
         "count_journey":"7",
         "type":"representative",
         "events":[
            {
               "trip_main_purpose":"Visiting the shop"
            },
            {
               "trip_main_purpose":"Testing the product"
            },
            {
               "trip_main_purpose":"Sharing on social network"
            },
            {
               "trip_main_purpose":"Visiting the shop2"
            }
         ]
      },
      "2":{
         "count_pattern":"6",
         "count_journey":"7",
         "type":"representative",
         "events":[
            {
               "trip_main_purpose":"Visiting the shop"
            },
            {
               "trip_main_purpose":"Testing the product"
            },
            {
               "trip_main_purpose":"Sharing on social network"
            }
         ]
      },
      "3":{
      '''
#for seq in seqs:
