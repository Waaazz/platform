from biens.models import Article
import decimal
def run():
    for i in range(5,10):
        article=Article()
        article.nom="Article N° #%d" %i
        article.description="Description article  N° %d" %i
        article.image="http://defauft"
        prix = decimal.Decimal(i)  # Par exemple, si le prix est simplement l'itération actuelle
        article.prix = prix
        article.save()
print("Opération réussie")