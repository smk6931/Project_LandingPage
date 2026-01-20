import PortfolioCard from '../components/PortfolioCard';
import './Portfolio.css';

const Portfolio = () => {
  const projects = [
    {
      title: '럭셔리 호텔 예약 사이트',
      description: '프리미엄 호텔 체인을 위한 예약 및 멤버십 통합 플랫폼',
      imageUrl: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['아임웹', '반응형', 'SEO 최적화']
    },
    {
      title: '프리미엄 카페 브랜드',
      description: '오프라인 매장과 온라인 몰을 연동한 통합 브랜드 사이트',
      imageUrl: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['커스텀 개발', '온라인 쇼핑몰', 'CMS']
    },
    {
      title: '부동산 중개 플랫폼',
      description: '지도 기반 매물 검색 및 VR 투어 기능 제공',
      imageUrl: 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['React', 'Google Maps API', 'VR 통합']
    },
    {
      title: '뷰티 살롱 예약 시스템',
      description: '실시간 예약, 스타일리스트 추천, 고객 히스토리 관리',
      imageUrl: 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['아임웹', '예약 시스템', '모바일 최적화']
    },
    {
      title: '법률 사무소 포트폴리오',
      description: '신뢰감 있는 디자인과 상담 예약 자동화',
      imageUrl: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['워드프레스', '다국어 지원', '챗봇']
    },
    {
      title: '헬스케어 스타트업',
      description: 'AI 기반 건강 관리 서비스 랜딩페이지',
      imageUrl: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&h=400&fit=crop',
      link: 'https://example.com',
      tags: ['Next.js', ' 애니메이션', 'AI 통합']
    }
  ];

  return (
    <section className="portfolio" id="portfolio">
      <div className="container">
        <div className="section-header fade-in">
          <h2 className="section-title">포트폴리오</h2>
          <p className="section-subtitle">
            다양한 업종에서 검증된 우리의 실력을 확인하세요
          </p>
        </div>

        <div className="portfolio-grid">
          {projects.map((project, index) => (
            <PortfolioCard key={index} {...project} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Portfolio;
