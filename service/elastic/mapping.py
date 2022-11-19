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
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
            }
        }
# fmt: on
