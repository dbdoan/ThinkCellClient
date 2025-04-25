import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import IntroComponent from './components/TypingEffect.jsx'

function App() {
  const [count, setCount] = useState(0)

    return (
      <>
      <div className="top-text">
        <div className="typing-effect-intro">
          <IntroComponent />
        </div>
        <div className="developed-by">
          <h2>
            by <span class="name-highlight">Danny Doan</span>
          </h2>
        </div>

      </div>

      <div className="card">
        <p>
          test sentence
        </p>
      </div>
      <p className="read-the-docs">
        {/* Click on the Vite and React logos to learn more */}
      </p>
    </>
  )
}

export default App
