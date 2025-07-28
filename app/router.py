from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex
import logging

# Set up logging to debug the router
logging.basicConfig(level=logging.INFO)

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-mpnet-base-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "What is your return policy?",
        "How do I return a product?",
        "What's your policy on defective products?",
        "Do you offer cash on delivery?",
        "How can I contact customer service?",
        "What are your shipping options?",
        "Do you ship internationally?",
        "How long does shipping take?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "Show me Nike shoes",
        "Find shoes with high ratings",
        "What are the best running shoes?",
        "Show me shoes from Adidas",
        "I'm looking for sports shoes",
        "What shoes are on discount?",
        "Find me shoes under 2000 rupees",
        "Show me the most popular shoes",
        "What are the cheapest shoes you have?",
        "Find me shoes with 4+ rating",
    ]
)

index = LocalIndex()

# Remove the unused router_config line
router = SemanticRouter(
    routes=[faq, sql],
    encoder=encoder,
    index=index,
    auto_sync="local"
)

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)