import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


def quote(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html',
                  {"tags": tags, 'form': QuoteForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote})


def authordetail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/authordetail.html', {"author": author})


def migrate_db(request):
    parse()
    add_to_db()
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


def add_to_db():
    for a in authors:
        date = datetime.strptime(a["born_date"], "%B %d, %Y")
        try:
            Author.objects.get(fullname=a["fullname"])
        except Author.DoesNotExist:
            Author(fullname=a["fullname"], born_date=date,
                   born_location=a["born_location"], description=a["description"]).save()
        else:
            continue
    for q in quotes_lst:
        try:
            Quote.objects.get(quote=q["quote"])
        except Quote.DoesNotExist:
            print(q["quote"])
            author_for_quote = Author.objects.get(fullname=q["author"])
            Quote(quote=q["quote"], author=author_for_quote).save()
            quote = Quote.objects.get(quote=q["quote"])
            tags = q["tags"]
            for tag in tags:
                try:
                    tag_for_quote = Tag.objects.get(name=tag)
                    quote.tags.add(tag_for_quote)
                except Tag.DoesNotExist:
                    Tag(name=tag).save()
                    made_tag = Tag.objects.get(name=tag)
                    quote.tags.add(made_tag)


def parse():
    for page in range(10):
        response = requests.get(f"{domain}/page/{page + 1}/")
        parse_cards(response)


domain = "https://quotes.toscrape.com"
quotes_lst = []
authors = []
authors_rdy = []


def parse_cards(link):
    soup = BeautifulSoup(link.text, "lxml")
    quotes = soup.find_all("div", class_="quote")
    for quote_card in quotes:
        quote = quote_card.find("span", class_="text").text
        author = quote_card.find("small", class_="author").text
        author = author.replace("-", " ")
        tags_lst = quote_card.find_all("a", class_="tag")
        tags = []
        for tag in tags_lst:
            tags.append(tag.text)
        quote_dict = {"tags": tags, "author": author, "quote": quote}
        quotes_lst.append(quote_dict)
        if author not in authors_rdy:
            link = quote_card.find("a")
            parse_author(f"{domain}{link['href']}")


def parse_author(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    name = soup.find("h3", class_="author-title").text
    name = name.replace("-", " ")
    born_date = soup.find("span", class_="author-born-date").text
    born_loc = soup.find("span", class_="author-born-location").text
    description = soup.find("div", class_="author-description")
    description = description.text.strip()
    pos = re.search("(More: http)", description)
    if pos:
        author = {"fullname": name, "born_date": born_date, "born_location": born_loc,
                  "description": description[:pos.span()[0]]}
    else:
        author = {"fullname": name, "born_date": born_date, "born_location": born_loc,
                  "description": description}
    authors_rdy.append(name)
    authors.append(author)
