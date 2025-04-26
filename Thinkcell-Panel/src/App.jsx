
import './App.css'
import { useState } from 'react'
// import linkedInLogo from './assets/linkedin.svg'
// import githubLogo from './assets/github.svg'
import IntroComponent from './components/TypingEffect.jsx'
import { handleKeyFileChange, handleTemplateFileChange } from './components/fileValidator.js'

import LinkedInIcon from './components/linkedinLogo.jsx';
import GithubIcon from './components/githubLogo.jsx';

function App() {
  const [count, setCount] = useState(0)

  function handleSubmit(e) {
    e.preventDefault();
    console.log("Files successfully submitted");
  }


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
        <form id="upload-form" onSubmit={handleSubmit}>
          <p className="instructions">To generate a Thinkcell PPTX, 2 files are needed:</p>
          <p>1. PPTTC (key) or a properly formatted CSV</p>
          <input className="choose-file" type="file" name="jsonFile" accept=".ppttc, .csv" onChange={ handleKeyFileChange }/>
          <p>2. PPTTC Template</p>
          <input className="choose-file" type="file" name="ppttcFile" accept=".ppttc" onChange={ handleTemplateFileChange } />
          <button className="submit-btn" type="submit">Upload</button>
        </form>
        <div className="output">

        </div>
      </div>
      
      <div className="footer">
        <a className="social-logo" href="https://www.linkedin.com/in/dbdoan/" target="_blank" rel="noreferrer" alt="button to LinkedIn profile">
          <LinkedInIcon />
        </a>

        <a className="social-logo" href="https://github.com/dbdoan/ThinkCellClient" target="_blank" rel="noreferrer" alt="button to Github source code">
          <GithubIcon />
        </a>
      </div>
    </>
  )
}

export default App
