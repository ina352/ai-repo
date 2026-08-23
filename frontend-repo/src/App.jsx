import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    store_type: '감성 카페',
    menu: '딸기 생크림 케이크',
    event: '10% 할인',
    style: '친근하고 감성적인 말투'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-text', formData);
      setResult(response.data);
    } catch (error) {
      console.error("생성 실패:", error);
      alert("백엔드 서버 연동 실패! backend-repo에서 uvicorn 서버가 켜져 있는지 확인해 주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>소상공인 AI 홍보물 자동 제작 플랫폼</h2>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '30px' }}>
        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>업종</label>
          <input type="text" name="store_type" value={formData.store_type} onChange={handleChange} style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} required />
        </div>

        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>대표 메뉴 / 상품</label>
          <input type="text" name="menu" value={formData.menu} onChange={handleChange} style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} required />
        </div>

        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>이벤트 / 할인 정보</label>
          <input type="text" name="event" value={formData.event} onChange={handleChange} style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} required />
        </div>

        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>원하는 분위기 / 말투</label>
          <input type="text" name="style" value={formData.style} onChange={handleChange} style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} required />
        </div>

        <button type="submit" disabled={loading} style={{ padding: '12px', backgroundColor: loading ? '#ccc' : '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px', cursor: loading ? 'not-allowed' : 'pointer', marginTop: '10px' }}>
          {loading ? 'AI가 홍보 문구를 작성 중입니다...' : 'AI 홍보 문구 생성하기'}
        </button>
      </form>

      {result && (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
          <h3 style={{ color: '#2c3e50', marginTop: 0 }}>🎉 생성된 AI 홍보 결과</h3>
          <div style={{ marginBottom: '15px' }}>
            <h4>📌 메인 헤드라인</h4>
            <p style={{ fontWeight: 'bold', fontSize: '18px', color: '#e74c3c' }}>{result.main_headline}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <h4>📝 상세 홍보 본문</h4>
            <p style={{ whiteSpace: 'pre-line', lineHeight: '1.6' }}>{result.body_content}</p>
          </div>
          <div>
            <h4>🏷️ 추천 해시태그</h4>
            <p style={{ color: '#2980b9' }}>
              {Array.isArray(result.hashtags) ? result.hashtags.join(' ') : result.hashtags}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;