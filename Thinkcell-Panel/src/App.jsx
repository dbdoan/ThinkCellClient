import { useState } from 'react'
import './App.css'
import IntroComponent from './components/TypingEffect.jsx'
import { handleKeyFileChange, handleTemplateFileChange } from './components/fileValidator.js';

import './App.scss';

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
            by <span className="name-highlight">Danny Doan</span>
          </h2>
        </div>

      </div>

      <div className="card">
        <form id="upload-form">
          <p className="instructions">To generate a Thinkcell PPTX, 2 files are needed:</p>
          <p>1. PPTTC (key) OR a properly formatted CSV</p>
          <input className="choose-file" type="file" name="jsonFile" accept=".ppttc, .csv" onChange={ handleKeyFileChange }/>
          <p>2. PPTTC Template</p>
          <input className="choose-file" type="file" name="ppttcFile" accept=".ppttc" onChange={ handleTemplateFileChange } />
          <button className="submit-btn" type="submit">Upload</button>
        </form>
      </div>
    </>
  )
}

export default App
