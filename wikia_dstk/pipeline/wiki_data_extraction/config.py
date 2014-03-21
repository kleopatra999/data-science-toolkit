config = {
    "region": "us-west-2",
    "price": "0.300",
    "ami": "ami-d6e785e6",
    "key": "data-extraction",
    "sec": "sshable",
    "type": "m2.4xlarge",
    "tag": "wiki_data_extraction",
    "threshold": 50,
    "max_size": 5,
    "services": ",".join([
        "TopEntitiesService",
        "EntityDocumentCountsService",
        "TopHeadsService",
        "WpTopEntitiesService",
        "WpEntityDocumentCountsService",
        "WikiEntitySentimentService",
        "WpWikiEntitySentimentService",
        "AllEntitiesSentimentAndCountsService"
    ])
}