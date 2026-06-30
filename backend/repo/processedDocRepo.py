from db.dynamoDb import getTable
from schema.documentSchema import ProcessedDocSchema
from constant.appConstants import DYNAMODB_PROCESSED_DOCS_TABLE

def docAlreadyProcessed(docId: str) -> bool:
    table    = getTable(DYNAMODB_PROCESSED_DOCS_TABLE)
    response = table.get_item(Key={"docId": docId})
    return "Item" in response

def insertProcessedDoc(docData: ProcessedDocSchema) -> ProcessedDocSchema:
    table = getTable(DYNAMODB_PROCESSED_DOCS_TABLE)
    table.put_item(Item=docData.model_dump())
    return docData
