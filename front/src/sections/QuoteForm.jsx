import { useState } from 'react';
import Button from '../components/Button';
import './QuoteForm.css';

const QuoteForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    projectType: '',
    budget: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('견적 문의가 접수되었습니다!\n빠른 시일 내에 연락드리겠습니다.');
    console.log('Form Data:', formData);
  };

  return (
    <section className="quote-form" id="quote">
      <div className="container">
        <div className="section-header fade-in">
          <h2 className="section-title">견적 문의</h2>
          <p className="section-subtitle">
            프로젝트에 대해 자세히 알려주세요. 24시간 내 답변드립니다.
          </p>
        </div>

        <form className="form fade-in" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>이름 *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="홍길동"
                required
              />
            </div>

            <div className="form-group">
              <label>회사명</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="(주)회사명"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>이메일 *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="example@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label>연락처 *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="010-1234-5678"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>프로젝트 유형 *</label>
              <select
                name="projectType"
                value={formData.projectType}
                onChange={handleChange}
                required
              >
                <option value="">선택해주세요</option>
                <option value="imweb">아임웹 기반 제작</option>
                <option value="custom">완전 커스텀 개발</option>
                <option value="redesign">리디자인/리뉴얼</option>
                <option value="landing">랜딩페이지</option>
                <option value="ecommerce">쇼핑몰</option>
              </select>
            </div>

            <div className="form-group">
              <label>예산 범위</label>
              <select
                name="budget"
                value={formData.budget}
                onChange={handleChange}
              >
                <option value="">선택해주세요</option>
                <option value="under-300">300만원 미만</option>
                <option value="300-500">300~500만원</option>
                <option value="500-1000">500~1000만원</option>
                <option value="over-1000">1000만원 이상</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>프로젝트 상세 내용 *</label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="프로젝트에 대해 자세히 설명해주세요.&#10;- 원하시는 기능&#10;- 참고 사이트 URL&#10;- 목표 완료 시기&#10;- 기타 요구사항"
              rows="6"
              required
            ></textarea>
          </div>

          <div className="form-submit">
            <Button type="submit" size="lg">
              견적 문의 보내기
            </Button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default QuoteForm;
