import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    distribution = {}

    links = corpus[page]
    if not links:
        # No links from the current page — treat it as linking to every page
        return {p: 1 / N for p in corpus}

    for p in corpus:
        distribution[p] = (1 - damping_factor) / N
        if p in links:
            distribution[p] += damping_factor / len(links)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = random.choice(list(corpus.keys()))

    result = {p:0 for p in corpus}

    result[current_page] += 1

    for _ in range(n-1):
        rank = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(rank.keys()),
            weights=list(rank.values()),
            k=1
        )[0]

        result[current_page] += 1


    return {p:result[p]/n for p in result}



def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    threshold = 0.001
    pagerank = {page: 1 / N for page in corpus}

    while True:
        new_pagerank = {}
        for page in corpus:
            rank_sum = 0
            for other_page in corpus:
                links = corpus[other_page]
                if not links:
                    # Treat as linking to every page
                    links = set(corpus.keys())
                if page in links:
                    rank_sum += pagerank[other_page] / len(links)

            new_pagerank[page] = (1 - damping_factor) / N + damping_factor * rank_sum

        # Check for convergence
        if all(abs(new_pagerank[p] - pagerank[p]) < threshold for p in pagerank):
            break
        pagerank = new_pagerank

    # Normalize to ensure they sum to 1
    total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total

    return pagerank


if __name__ == "__main__":
    main()
