import Hero from './sections/Hero';
import Portfolio from './sections/Portfolio';
import Process from './sections/Process';
import Guidelines from './sections/Guidelines';
import QuoteForm from './sections/QuoteForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <Portfolio />
      <Process />
      <Guidelines />
      <QuoteForm />

      <footer className="footer">
        <p>&copy; 2026 Web Design Studio. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
