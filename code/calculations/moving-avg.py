import pandas as pd
from pymongo import MongoClient

pd.options.mode.chained_assignment = None


client = MongoClient(
    "mongodb+srv://yorkU:yorkuresearch@cluster0.7dorbhd.mongodb.net/?retryWrites=true&w=majority"
)
print("db connected")
mydb = client["Raw_data"]
mycol = mydb["2021_data"]


df = mycol.find(
    {}, {"Timestamp", "height", "difficulty", "poolname"}
)  # get the parameters we need for our calculations and store them in a dataframe
df1 = pd.DataFrame(df)
# print(df1)
df1 = df1.set_index("Timestamp")  # set index to Timestamp
# print(df1)
df1.index = pd.to_datetime(df1.index)
df1["original_position"] = range(
    0, 0 + len(df1)
)  # additional index 'original_position' to keep track of the back-calculation to 720 blocks
df1.sort_values(by=["original_position"], inplace=True)
# print(df1)
idx = df1.index.floor("24H")
df2 = df1[~idx.duplicated(keep="last")]  # get the last block from each day
##print(df2)
# df2.to_csv('last-blocks21.csv', encoding='utf-8', index=False)
df2.set_index("original_position")
##print(df2)

last_occurance_idx = (
    53936  # from df2, get the last occurance index for each block that appears
)
last_pos = df1.loc[df1["original_position"] == last_occurance_idx].to_numpy()[
    0
]  # match with original_position to get the last position of the block in the whole dataset
# to_numpy() to convert into series
x = last_pos[4]  # extract the original_position
###print(x)
cap = x - 720  # get the previous 720 blocks
##
##
select_idx = df1.loc[
    df1["original_position"].isin(list(range(cap, x)))
].index  # get the range of 720 blocks data according to the last_occurance_idx
rangedata = df1.loc[select_idx, :]
# print(rangedata['difficulty'])
# rangedata.to_csv('diff.csv',encoding='utf-8')
success_rate = rangedata.groupby("poolname")[
    "poolname"
].count()  # get the success rate by running count operation
# print(success_rate)
#
freq_dict = success_rate.to_dict()
##print(freq_dict)
pblocks = freq_dict.get(last_pos[3])  # extract success rate for the 720 block range
print(pblocks)
diff1 = rangedata["difficulty"].mean()  # if no change in difficulty in rangedata
# diff = (2.060880e+13*(602/720) +2.504650e+13*(118/720)) ##if you see changes in difficulty values, apply this method
# to get diff

# print(diff)
print(diff1)

#
# hashrate = (pblocks/720)*(diff*2**32)/(600*10**18)
hashrate1 = (
    (pblocks / 720) * (diff1 * 2**32) / (600 * 10**18)
)  # calcutlate hashrate

print(last_occurance_idx)
# print(hashrate)
print(hashrate1)
# df2.loc[(df2['original_position']== last_occurance_idx), 'hashrate'] = hashrate
# df2.to_csv('test21.csv',encoding='utf-8')
# df2.to_json('daily_ph.json')


# print(df2)
