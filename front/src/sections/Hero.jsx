import Button from '../components/Button';
import './Hero.css';

const Hero = () => {
  const scrollToQuote = () => {
    document.getElementById('quote')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="hero">
      <div className="hero-bg">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <div className="hero-content fade-in">
        <div className="hero-badge">
          <span>✨ Premium Web Design Studio</span>
        </div>

        <h1 className="hero-title">
          당신의 비즈니스를<br />
          <span className="gradient-text">프리미엄 웹사이트</span>로
        </h1>

        <p className="hero-description">
          아임웹 기반 맞춤 제작부터 완전 커스텀 개발까지.<br />
          당신의 아이디어를 현실로 만들어드립니다.
        </p>

        <div className="hero-buttons">
          <Button size="lg" onClick={scrollToQuote}>
            견적 문의하기
          </Button>
          <Button variant="secondary" size="lg">
            포트폴리오 보기
          </Button>
        </div>

        <div className="hero-stats">
          <div className="stat">
            <h3>50+</h3>
            <p>완료 프로젝트</p>
          </div>
          <div className="stat">
            <h3>98%</h3>
            <p>고객 만족도</p>
          </div>
          <div className="stat">
            <h3>3일</h3>
            <p>평균 제작 기간</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
