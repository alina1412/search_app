# fmt: off
MAPPING_FOR_INDEX = {
            "properties": {
                "id": {
                    "type": "integer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "message": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "search_analyzer": "standard",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
            }
        }

elastic_text_settings = {
    "analysis": {
        "filter": {
            "ngram_filter": {
            "type": "ngram",
            "min_gram": 4,
            "max_gram": 20
            }
      },
      "analyzer": {
        "ngram_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "ngram_filter"
          ]
        }
      }
    },
    "max_ngram_diff": 50
}
# fmt: on
