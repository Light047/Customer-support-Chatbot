from google.cloud import dialogflow_v2 as dialogflow

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(parent, intent)
    print('Intent created: {}'.format(response))

def create_entity(project_id, display_name, entity_values):
    entities_client = dialogflow.EntityTypesClient()
    parent = entities_client.project_agent_path(project_id)

    entity = dialogflow.types.EntityType.Entity()
    entity.display_name = display_name
    entity.kind = dialogflow.types.EntityType.Kind.KIND_MAP

    for entity_value in entity_values:
        entity_entry = dialogflow.types.EntityType.Entity.EntityEntry(value=entity_value, synonyms=[entity_value])
        entity.entities.append(entity_entry)

    response = entities_client.create_entity_type(parent, dialogflow.types.EntityType(display_name=display_name, entities=[entity]))
    print('Entity created: {}'.format(response))

def setup_webhook(project_id, webhook_url):
    agent_client = dialogflow.AgentsClient()
    parent = agent_client.project_path(project_id)

    agent = agent_client.get_agent(parent)
    agent.default_webhook_url = webhook_url

    response = agent_client.update_agent(agent)
    print('Webhook URL set: {}'.format(response))

# Example usage
project_id = 'customersupportchatbot-425715pi'
webhook_url = 'https://xtreme47.pythonanywhere.com/'

# Create intents
create_intent(project_id, 'Order Tracking', ['Track my order', "Where's my package?"], ['Here is the tracking information for your order.'])
create_intent(project_id, 'Return Policy', ['Return policy', 'How do I return an item?'], ['Our return policy allows...'])

# Create entities
create_entity(project_id, 'Order Number', ['123456', '789012'])
create_entity(project_id, 'Product Name', ['Product X', 'Product Y'])

# Set up webhook fulfillment
setup_webhook(project_id, webhook_url)
