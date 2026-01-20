import './PortfolioCard.css';

const PortfolioCard = ({ title, description, imageUrl, link, tags }) => {
  return (
    <div className="portfolio-card" onClick={() => window.open(link, '_blank')}>
      <div className="card-image">
        <img src={imageUrl} alt={title} />
        <div className="card-overlay">
          <span className="view-project">프로젝트 보기 →</span>
        </div>
      </div>
      <div className="card-content">
        <h3>{title}</h3>
        <p>{description}</p>
        <div className="card-tags">
          {tags.map((tag, index) => (
            <span key={index} className="tag">{tag}</span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PortfolioCard;
