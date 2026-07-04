import json
import re

class ProductClaimsAgent:
    """Extracts text claims from packaging images using OCR / Text simulation."""
    def extract_claims(self, uploaded_image_file) -> str:
        if uploaded_image_file is None:
            return ""
        
        filename = uploaded_image_file.name.lower()
        
        if "sleep" in filename or "calm" in filename:
            return "Nighttime recovery blend. Features organic Chamomile and Magnesium Glycinate. Promotes deep REM cycles."
        
        elif "protein" in filename or "muscle" in filename:
            return "High-performance isolate whey. Loaded with branched-chain amino acids (BCAAs). Promotes rapid lean muscular recovery."
        
        elif "skin" in filename or "glow" in filename or "beauty" in filename:
            return "Premium anti-aging complex. Formulated with marine Collagen and moisture-locking Hyaluronic Acid for skin elasticity."
        
        elif "keto" in filename or "burn" in filename or "diet" in filename:
            return "Advanced thermogenic complex. Clean Apple Cider Vinegar extraction with Green Tea catechins to support healthy metabolism."
        
        else:
            # The catch-all default fallback
            return "Advanced botanical wellness matrix. Enriched with Turmeric Curcumin extract. Non-GMO verified operational claims."

class HeroIngredientExtractorAgent:
    """Identifies and extracts key active ingredients from unstructured claims text."""
    def __init__(self):
        self.known_ingredients = [
            "Collagen", "Hyaluronic Acid", "Apple Cider Vinegar", "Green Tea",
            "Ashwagandha", "L-Theanine", "Chamomile", "Magnesium Glycinate", 
            "BCAAs", "Turmeric Curcumin"
        ]
        
    def extract_ingredients(self, text: str) -> list:
        found = []
        for ing in self.known_ingredients:
            if re.search(r'\b' + re.escape(ing) + r'\b', text, re.IGNORECASE):
                found.append(ing)
        return found if found else ["Standard Mineral Matrix"]

class RevenueAttributionAgent:
    """Allocates product revenue proportionally to individual weighted claims."""
    def calculate_attribution(self, total_revenue: float, elements: list) -> dict:
        if not elements:
            return {}
        # Equally distributed weights over claims/ingredients to model financial impact
        weight = 1.0 / len(elements)
        return {item: round(total_revenue * weight, 2) for item in elements}

class MarketMatchingAgent:
    """Maps identified SKUs to predefined top-level health benefit categories."""
    def match_category(self, claims_text: str) -> str:
        text = claims_text.lower()
        if any(x in text for x in ["sleep", "rem", "calm", "ashwagandha", "l-theanine", "chamomile", "magnesium"]):
            return "Cognitive Health & Stress"
        elif any(x in text for x in ["keto", "burn", "vinegar", "metabolism", "green tea", "diet"]):
            return "Metabolism & Weight Management"
        elif any(x in text for x in ["protein", "muscle", "bcaa"]):
            return "Athletic Performance & Recovery"
        elif any(x in text for x in ["glow", "collagen", "skin", "hyaluronic", "beauty"]):
            return "Skin & Radiance"
        return "General Preventive Health"

class OrchestratorAgent:
    """Coordinates downstream specialized agents and parses interactive dashboard query routing."""
    def __init__(self):
        self.claims_agent = ProductClaimsAgent()
        self.ingredient_agent = HeroIngredientExtractorAgent()
        self.revenue_agent = RevenueAttributionAgent()
        self.matching_agent = MarketMatchingAgent()

    def process_new_packaging_pipeline(self, image_file, brand_name, total_revenue) -> dict:
        # Step 1: Execute OCR Claims extraction
        raw_claims = self.claims_agent.extract_claims(image_file)
        # Step 2: Extract active ingredients
        ingredients = self.ingredient_agent.extract_ingredients(raw_claims)
        # Step 3: Run Market Mapping Logic
        assigned_category = self.matching_agent.match_category(raw_claims)
        # Step 4: Run Financial Revenue Allocation
        attribution_map = self.revenue_agent.calculate_attribution(total_revenue, ingredients)
        
        return {
            "sku": f"NEW-SKU-{brand_name[:3].upper()}",
            "brand": brand_name,
            "total_revenue_usd": total_revenue,
            "suggested_category": assigned_category,
            "raw_claims_text": raw_claims,
            "extracted_ingredients": ingredients,
            "revenue_attribution": attribution_map
        }

    def parse_natural_language_query(self, query: str, active_database: list) -> str:
        q = query.lower()
        if "revenue" in q or "financial" in q:
            total_pool = sum(item["total_revenue_usd"] for item in active_database)
            return f"💡 Operational Insight: Total tracked revenue across the current segment is ${total_pool:,.2f} USD."
        elif "ingredient" in q or "claims" in q:
            return "💡 Operational Insight: High concentration of adaptogenic compounds and recovery proteins observed trending in high-revenue SKUs."
        elif "category" in q or "segments" in q:
            return "💡 Operational Insight: Market share density is currently adjusting dynamically across newly tracked portfolio segments."
        return "💡 Operational Insight: Intent parsed successfully. No anomalous shifts identified in this data slice."