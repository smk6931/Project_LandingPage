import './Guidelines.css';

const Guidelines = () => {
  const guidelines = [
    {
      icon: '✏️',
      title: '수정 범위',
      items: [
        '초안 검토 후 2회 무료 수정',
        '추가 수정 시 건당 비용 발생',
        '기획 단계 변경은 별도 협의'
      ]
    },
    {
      icon: '⏱️',
      title: '제작 기간',
      items: [
        '아임웹 기반: 3~7일',
        '커스텀 개발: 2~4주',
        '긴급 요청 시 추가 비용'
      ]
    },
    {
      icon: '💰',
      title: '결제 조건',
      items: [
        '계약금 50% 선입금',
        '완료 후 잔금 50% 지불',
        '기업 고객은 세금계산서 발행'
      ]
    },
    {
      icon: '📝',
      title: '제공 자료',
      items: [
        '로고, 이미지 등 리소스 제공 필수',
        '텍스트 콘텐츠 사전 준비',
        '참고 사이트 URL 공유'
      ]
    },
    {
      icon: '🔒',
      title: '저작권',
      items: [
        '완료 후 소스 코드 이전',
        '디자인 및 콘텐츠 소유권 고객',
        '포트폴리오 게재 동의 필요'
      ]
    },
    {
      icon: '🛡️',
      title: 'A/S 정책',
      items: [
        '배포 후 1개월 무상 기술 지원',
        '버그 수정 및 긴급 패치 제공',
        '유지보수 계약 별도 가능'
      ]
    }
  ];

  return (
    <section className="guidelines" id="guidelines">
      <div className="container">
        <div className="section-header fade-in">
          <h2 className="section-title">작업 가이드라인</h2>
          <p className="section-subtitle">
            원활한 프로젝트 진행을 위해 꼭 확인해주세요
          </p>
        </div>

        <div className="guidelines-grid">
          {guidelines.map((guideline, index) => (
            <div key={index} className="guideline-card fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="guideline-icon">{guideline.icon}</div>
              <h3 className="guideline-title">{guideline.title}</h3>
              <ul className="guideline-list">
                {guideline.items.map((item, idx) => (
                  <li key={idx}>
                    <span className="bullet">→</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Guidelines;
