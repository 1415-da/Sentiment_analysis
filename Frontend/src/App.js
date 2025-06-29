import React, { useState } from "react";
import styled, { createGlobalStyle } from "styled-components";
import { FaChartLine, FaArrowUp, FaArrowDown } from "react-icons/fa";
import { motion, AnimatePresence } from "framer-motion";

const GlobalStyle = createGlobalStyle`
  body {
    background: linear-gradient(120deg, #232526 0%, #414345 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    color: #fff;
    overflow-x: hidden;
  }
`;

const Ticker = styled.div`
  position: fixed;
  top: 0;
  width: 100vw;
  background: rgba(30, 30, 30, 0.95);
  color: #0f0;
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.1rem;
  padding: 0.3rem 0;
  z-index: 10;
  overflow: hidden;
  white-space: nowrap;
  animation: ticker 30s linear infinite;
  @keyframes ticker {
    0% { transform: translateX(100vw);}
    100% { transform: translateX(-100vw);}
  }
`;

const Container = styled.div`
  max-width: 500px;
  margin: 100px auto 0 auto;
  background: rgba(34, 40, 49, 0.95);
  border-radius: 18px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  padding: 2.5rem 2rem 2rem 2rem;
  text-align: center;
`;

const Header = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
`;

const SubHeader = styled.p`
  color: #aaa;
  font-size: 1.1rem;
  margin-bottom: 2rem;
`;

const Input = styled.textarea`
  width: 100%;
  min-height: 80px;
  border-radius: 10px;
  border: none;
  padding: 1rem;
  font-size: 1.1rem;
  background: #232931;
  color: #fff;
  margin-bottom: 1.5rem;
  resize: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: box-shadow 0.2s;
  &:focus {
    outline: none;
    box-shadow: 0 0 0 2px #00ff99;
  }
`;

const Button = styled.button`
  background: linear-gradient(90deg, #00ff99 0%, #00c3ff 100%);
  color: #232931;
  font-weight: bold;
  font-size: 1.1rem;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2.2rem;
  cursor: pointer;
  margin-top: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,255,153,0.1);
  transition: background 0.2s, color 0.2s;
  &:hover {
    background: linear-gradient(90deg, #00c3ff 0%, #00ff99 100%);
    color: #fff;
  }
`;

const ResultCard = styled(motion.div)`
  margin-top: 2rem;
  padding: 1.5rem 1rem;
  border-radius: 12px;
  font-size: 1.3rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: ${({ sentiment }) =>
    sentiment === 1
      ? "rgba(0,255,153,0.15)"
      : sentiment === -1
      ? "rgba(255,0,80,0.15)"
      : "rgba(255,255,255,0.08)"};
  color: ${({ sentiment }) =>
    sentiment === 1
      ? "#00ff99"
      : sentiment === -1
      ? "#ff0050"
      : "#fff"};
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
`;

const resultVariants = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -30 }
};

const tickers = [
  "AAPL +1.23%", "GOOG -0.45%", "TSLA +2.10%", "AMZN +0.67%", "MSFT -0.12%", "META +1.01%", "NFLX -0.89%", "NVDA +3.45%"
];

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [sentiment, setSentiment] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setSentiment(0);
    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setSentiment(data.sentiment);
      if (data.sentiment === 1) setResult("Positive Sentiment");
      else if (data.sentiment === -1) setResult("Negative Sentiment");
      else setResult("Neutral or Unknown");
    } catch {
      setResult("Error: Could not connect to backend.");
    }
    setLoading(false);
  };

  return (
    <>
      <GlobalStyle />
      <Ticker>
        {tickers.map((t, i) => (
          <span key={i} style={{ marginRight: 40 }}>{t}</span>
        ))}
      </Ticker>
      <Container>
        <Header>
          <FaChartLine style={{ color: "#00ff99" }} />
          Stock Market Sentiment Analyzer
        </Header>
        <SubHeader>
          Enter a news headline, tweet, or your own text about the stock market.<br />
          Our AI will tell you if the sentiment is <span style={{ color: "#00ff99" }}>positive</span> or <span style={{ color: "#ff0050" }}>negative</span>.
        </SubHeader>
        <form onSubmit={handleSubmit}>
          <Input
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="e.g. Tesla shares soar after earnings beat expectations"
            required
            disabled={loading}
          />
          <Button type="submit" disabled={loading || !text.trim()}>
            {loading ? "Analyzing..." : "Analyze"}
          </Button>
        </form>
        <AnimatePresence>
          {result && (
            <ResultCard
              sentiment={sentiment}
              variants={resultVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={{ duration: 0.5 }}
            >
              {sentiment === 1 && <FaArrowUp size={28} />}
              {sentiment === -1 && <FaArrowDown size={28} />}
              {result}
            </ResultCard>
          )}
        </AnimatePresence>
      </Container>
    </>
  );
}

export default App; 