import './Process.css';

const Process = () => {
  const steps = [
    {
      number: '01',
      title: '상담 & 견적',
      description: '고객님의 요구사항을 상세히 파악하고 최적의 솔루션과 견적을 제안합니다.',
      icon: '💬'
    },
    {
      number: '02',
      title: '기획 & 디자인',
      description: '와이어프레임 작성, UI/UX 디자인, 프로토타입 제작을 진행합니다.',
      icon: '🎨'
    },
    {
      number: '03',
      title: '개발 & 구현',
      description: '최신 기술 스택으로 빠르고 안정적인 웹사이트를 개발합니다.',
      icon: '⚡'
    },
    {
      number: '04',
      title: '테스트 & 수정',
      description: '크로스 브라우징, 반응형, 성능 테스트 후 피드백을 반영합니다.',
      icon: '🔍'
    },
    {
      number: '05',
      title: '배포 & 교육',
      description: '서버 배포, 도메인 연결, 관리자 교육까지 완벽하게 지원합니다.',
      icon: '🚀'
    },
    {
      number: '06',
      title: 'A/S & 유지보수',
      description: '배포 후에도 지속적인 기술 지원과 업데이트를 제공합니다.',
      icon: '🛠️'
    }
  ];

  return (
    <section className="process" id="process">
      <div className="container">
        <div className="section-header fade-in">
          <h2 className="section-title">작업 프로세스</h2>
          <p className="section-subtitle">
            체계적인 6단계 프로세스로 완벽한 결과물을 보장합니다
          </p>
        </div>

        <div className="process-timeline">
          {steps.map((step, index) => (
            <div key={index} className="process-step fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="step-number">{step.number}</div>
              <div className="step-icon">{step.icon}</div>
              <div className="step-content">
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </div>
              {index < steps.length - 1 && <div className="step-connector"></div>}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Process;
