import './Button.css';

const Button = ({ children, variant = 'primary', size = 'md', onClick, disabled, className = '' }) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
