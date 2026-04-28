from fastapi import FastAPI, HTTPException
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="API de recommendation", 
    description="Moteur de recommandation d'articles hybride"
)


embed_40 = np.load("embeddings.npy")

with open("user_activity_dict.json", "r") as f:
    user_history = json.load(f)

with open("old_artcl_id.json", "r") as f:
    old_artcl_ids = json.load(f)

with open("most_5_popular_recent_artcl.json", "r") as f:
    top_5_popular = json.load(f)



@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str):

    try:
        user_artcl = user_history.get(user_id, [])
        
        if len(user_artcl) == 0:
            return {
                "user_id": user_id, 
                "type_reco": "trending_fallback", 
                "articles": top_5_popular
            }
    
        user_embeds = embed_40[user_artcl]
        user_vec_mean = user_embeds.mean(axis=0).reshape(1, -1)
        
        user_sim = cosine_similarity(user_vec_mean, embed_40)[0]
        
        user_sim[old_artcl_ids] = -1.0
        
        user_sim[user_artcl] = -1.0
        
        user_top_5 = [int(idx) for idx in np.argsort(user_sim)[-5:][::-1]]
        
        return {
            "user_id": user_id, 
            "type_reco": "content_based", 
            "articles": user_top_5
        }
        
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")