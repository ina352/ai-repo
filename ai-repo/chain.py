import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=api_key)

# 1. 출력받을 JSON 스키마 정의
class PromoOutput(BaseModel):
    main_headline: str = Field(description="소비자의 눈길을 사로잡는 한 줄 카피")
    body_content: str = Field(description="본문 상세 설명 및 이벤트 정보")
    hashtags: list[str] = Field(description="추천 해시태그 5개 이상 목록")

# 2. JSON 파서 생성
parser = JsonOutputParser(pydantic_object=PromoOutput)

# 3. 프롬프트 템플릿 작성
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

# 4. 체인 연결 (프롬프트 -> LLM -> JSON 파서)
chain = prompt | llm | parser

def generate_promo_text(store_type, menu, event, style):
    return chain.invoke({
        "store_type": store_type,
        "menu": menu,
        "event": event,
        "style": style
    })

if __name__ == "__main__":
    result = generate_promo_text("감성 카페", "딸기 생크림 케이크", "10% 할인", "친근한 말투")
    print("\n=== 구조화된 AI 응답 데이터 ===")
    print(result)