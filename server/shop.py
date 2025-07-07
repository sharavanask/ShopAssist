import httpx 
from mcp.server.fastmcp import FastMCP
import re
from dotenv import load_dotenv
import os
load_dotenv()


mcp=FastMCP("shopassist") 

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct" 
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
X_RAPIDAPI_KEY=os.getenv("x-rapidapi-key")

def summarize_product(product,option):
    if option==1:
        return(
            f"ASIN:{product.get("asin")}\n"
            f"Product: {product.get('product_title', 'N/A')}\n"
            f"Category: {product.get('product_category', 'N/A')}\n"
            f"Rating: {product.get('product_star_rating', 'N/A')} stars "
            f"({product.get('product_num_ratings', 'N/A')} ratings)\n"
            f"Price: {product.get('product_price', 'N/A')}\n"
            f"URL: {product.get('product_url', 'N/A')}\n"
        )
    elif option==2:
        return(
            f"ASIN:{product.get("asin")}\n"
            f"product_title:{product.get('product_title', 'N/A')}\n"
            f"product_info:{product.get('product_information',"N/A")}\n"
            f"product_description:{product.get('product_description',"N/A")}\n"
            f"product_details:{product.get('product_details',"N/A")}\n"
        )

@mcp.tool()
async def getproduct(
    prod:str,
    specific_features:str="",
    minp:float=1,
    maxp:float=9999999.0)->str:
    """
    This tools helps in get the product lisitng from the ecommerce sites
    accodrding to the input given by the user"""
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": X_RAPIDAPI_KEY,
	    "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }
    params={
        "query":prod,
        "page":1,
        "country":"IN",
        "sort_by":"RELEVANCE",
        "product_condition":"NEW",
        "min_price":str(minp),
        "max_price":str(maxp),
    }
    async with httpx.AsyncClient() as client:
        response=await client.get(url,headers=headers,params=params)
        response.raise_for_status
        data=response.json()
        products=data.get("data",{}).get("products",[])
        # return products
    summary=[]
    for i in products[:15]:
        summary.append(summarize_product(i,1))
    summary="\n\n".join(summary)
    finalrespone=await gettop3(summary,specific_features)
    return finalrespone

async def getasin(top3_summary:str)->str:
    return re.findall(r'ASIN[: ] ?([A-Z0-9]{10})', top3_summary)
    

async def compare(top3,specific_features):

    """"this toolhelps in creating a comparison chart to the user to get the best rpoduct to buy
    after considering all the features in a one on one basis"""
    asins= await getasin(top3)
    s=""
    for i in asins:
        s+=f"{getproductdetails(i)}\n"
    # prompt=f"""
    # You are the expert and a trained professional in shopping assistant.You have the info of the top 3 products of same category you r job is to create a 
    # comparison  of the top 3 products and return the best product info as given in {s}
    # consider the user requirements in it {specific_features}.You must recommend the products which is given here dont add anything by yourself.
    # """
    prompt=f"""You are a professional shopping assistant and product expert.

Your task is to:
1️⃣ Compare the following **top 3 products** in the same category:  
{top3}

2️⃣ Carefully consider the **user's specific requirements**:  
{specific_features}

3️⃣ Create a clear, structured comparison covering in a table format or image format:
   - Product Names along with url of the product
   - Key Specifications
   - Pros and Cons for each
   - How well each matches the user’s requirements

4️⃣ **Decide which product is the best choice** for the user based on the comparison and requirements.

5️⃣ Return only:
   - A brief summary of why it’s the best
   - The selected product’s name and key details

⚠️ **Important:**  
    - Do NOT invent any products or details not present in the {top3}.  
- Only use the information given.

Provide your answer in **clear bullet points or a short paragraph if needed**.
"""
    headers={
        "Authorization":f"Bearer {GROQ_API_KEY}",
        "Content-Type":"application/json"
    }
    payload={
        "model":MODEL_NAME,
        "messages":[
            {"role":"user","content":prompt}
        ],
        "temperature":0.7,
        # "max_tokens":
    }
    try:
        async with httpx.AsyncClient() as client:
            res=await client.post(f"{GROQ_BASE_URL}/chat/completions",headers=headers,json=payload)
            res.raise_for_status()
            data=res.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"    



# @mcp.tool()
async def gettop3(summary:str,specific_features:str="")->str:
    prompt = f"""
    You are a Expert in product advisor AI and  a shop assistant who helps in finding better product to shop.Your job is to pick the top 3 products from the list of products available here alone {summary} 
    consider the user requirements in it {specific_features} and return the top 3 products info as given in {summary} along with its ASIN number too DOnt even add or remove anythuing other than this you must return the top 3 from the list alone .
    """
    headers={
        "Authorization":f"Bearer {GROQ_API_KEY}",
        "Content-Type":"application/json"
        }
    payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }
    try:
        async with httpx.AsyncClient() as client:
            res=await client.post(f"{GROQ_BASE_URL}/chat/completions",headers=headers,json=payload)
            res.raise_for_status()
            data=res.json()
            top3= data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    comparesummary=await compare(top3,specific_features)
    return comparesummary
    
    

async def getproductdetails(asin:str)->str:
    """This tool helps in getting the product details and specification of the particular product

    """     
    url="https://real-time-amazon-data.p.rapidapi.com/product-details"

    headers = {
        'x-rapidapi-key':X_RAPIDAPI_KEY,
        'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
    }
    params={
        "asin":asin,
        "country":"IN",
    }
    async with httpx.AsyncClient() as client:
        response =await client.get(url,headers=headers,params=params)   
        response.raise_for_status()
        data=response.json()
        product=data.get("data",{})
        if not product:
            return "No product found"
        return summarize_product(product,2)
    

if __name__ == "__main__":
    mcp.run()
    