from openai import OpenAI

KEY = ''

client = OpenAI(api_key=KEY)
ids = ['batch_66f56a9d1d5081909e0a58eebc3cf169',
       'batch_66f56ab644e081908ed52881c4d4aef2',
       'batch_66f56ac608d88190a3260b92291e9f67',
       'batch_66f56ad714c081908543a2bbb18f2f02',
       'batch_66f56ae819f48190896c005feb99e61a',
       'batch_66f56af7e5f08190bf66b3033c1ae0e7',
       'batch_66f56b119f948190bb2aa7f357b71f0a',
       'batch_66f56b2254648190be5d7158cddbc710',
       'batch_66f7c529be8081908cc42c9c7c9ee65d',
       'batch_66f8023c30388190a453d96ac58a5d03'
       ]
for id in ids:
    batch_obj = client.batches.retrieve(id)
    # print(id,vars(batch_obj)["status"],vars(batch_obj)["output_file_id"])
    print("\'" + vars(batch_obj)["output_file_id"] + "\',")
