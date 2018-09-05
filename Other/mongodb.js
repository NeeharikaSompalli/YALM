db.getCollection('uniform').updateMany(
    { "accessFreq" : {$gt : 20} },
    {
         $set: { "tier": 2},
    }
)

db.getCollection('uniform').updateMany(
    { "accessFreq" : {$gt : 25} },
    {
         $set: { "tier": 2},
    }
)