import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

app = FastAPI(title="소상공인 AI 홍보물 제작 API")

# 프론트엔드 통신(CORS) 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI 모델 및 파서 설정
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=api_key)

class PromoOutput(BaseModel):
    main_headline: str = Field(description="소비자의 눈길을 사로잡는 한 줄 카피")
    body_content: str = Field(description="본문 상세 설명 및 이벤트 정보")
    hashtags: list[str] = Field(description="추천 해시태그 5개 이상 목록")

parser = JsonOutputParser(pydantic_object=PromoOutput)

prompt = PromptTemplate(
    template="""당신은 소상공인을 돕는 전문 마케터입니다.
아래 매장 정보를 바탕으로 SNS 홍보 문구를 작성해주세요.

- 업종: {store_type}
- 대표 메뉴/상품: {menu}
- 이벤트/할인 정보: {event}
- 분위기: {style}

{format_instructions}""",
    input_variables=["store_type", "menu", "event", "style"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

# 프론트엔드 요청 데이터 규격
class PromoRequest(BaseModel):
    store_type: str
    menu: str
    event: str
    style: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "소상공인 AI 홍보물 자동 제작 서버 작동 중"}

@app.post("/api/generate-text")
def generate_promo_text(req: PromoRequest):
    try:
        result = chain.invoke({
            "store_type": req.store_type,
            "menu": req.menu,
            "event": req.event,
            "style": req.style
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))