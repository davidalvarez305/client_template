from django.shortcuts import render
from django.db import connection
import os

def home(request):

    # Environment Variables
    domain = os.environ.get('DOMAIN')
    site_name = os.environ.get('SITE_NAME')
    logo = " ".join(site_name.lower())

    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT * FROM category;
        '''
    )
    rows = cursor.fetchall()
    columns = ["id", "title", "slug"]
    categories = [
        dict(zip(columns, row))
        for row in rows
    ]

    context = {
        "categories": categories,
        "domain": domain,
        "site_name": site_name,
        "logo": logo
    }

    return render(request, 'blog/home.html', context)

def category(request, *args, **kwargs):
    category_slug = kwargs['slug']

    # Environment Variables
    domain = os.environ.get('DOMAIN')
    site_name = os.environ.get('SITE_NAME')
    logo = " ".join(site_name.lower())

    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT CONCAT('single'),
        slug, title, description, horizontalcardproductimageurl, horizontalcardproductimagealt FROM review_post
        WHERE review_post."categoryId" = (
            SELECT id FROM category AS c WHERE c.slug = %s
        )
        ''', [category_slug, category_slug]
    )
    rows = cursor.fetchall()
    columns = ["type", "slug", "title", "description", "horizontalcardproductimageurl", "horizontalcardproductimagealt"]
    posts = [
        dict(zip(columns, row))
        for row in rows
    ]

    context = {
        "posts": posts,
        "domain": domain,
        "site_name": site_name,
        "logo": logo
    }

    return render(request, 'blog/category.html', context)

def review_post(request, *args, **kwargs):
    rp_slug = kwargs['slug']

    # Environment Variables
    domain = os.environ.get('DOMAIN')
    site_name = os.environ.get('SITE_NAME')
    logo = " ".join(site_name.lower())

    # Get Post Data
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT JSON_BUILD_OBJECT('post', (
            SELECT JSON_AGG(row_to_json(review_post)) AS post FROM review_post WHERE slug = %s
        ), 'related_rev', (
            SELECT JSON_AGG(TO_JSON(review_post)) AS related_rev FROM review_post WHERE "categoryId" = (
                SELECT "categoryId" FROM review_post AS rp WHERE rp.slug = %s
            ) GROUP BY "categoryId"
        ), 'product_info', (
            SELECT JSON_AGG(TO_JSON(product)) AS p FROM product WHERE "affiliateUrl" = (
                SELECT productaffiliateurl FROM review_post AS rp WHERE rp.slug = %s
            )
        )) AS review_post;
        ''', [rp_slug, rp_slug, rp_slug, rp_slug]
    )
    rows = cursor.fetchall()
    desc = cursor.description
    columns = [col[0] for col in desc]
    rev_post = [
        dict(zip(columns, row))
        for row in rows
    ]
    print(rev_post)

    # Get Product Information
    product_info = rev_post[0]['review_post']['product_info'][0]

    context = {
        "post": rev_post[0]['review_post']['post'][0],
        "product_info": product_info,
        "related_rev": rev_post[0]['review_post']['related_rev'],
        "type": "single",
        "domain": domain,
        "site_name": site_name,
        "logo": logo
    }

    return render(request, 'blog/review_post.html', context)