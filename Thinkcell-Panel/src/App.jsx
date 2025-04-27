
import './App.css'
import { useState } from 'react'
// import linkedInLogo from './assets/linkedin.svg'
// import githubLogo from './assets/github.svg'
import IntroComponent from './components/TypingEffect.jsx'

import LinkedInIcon from './components/linkedinLogo.jsx';
import GithubIcon from './components/githubLogo.jsx';

function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [keyFile, setKeyFile] = useState(null);
  const [templateFile, setTemplateFile] = useState(null);

  function handleTemplateFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.pptx')) {
      setTemplateFile(file);
      console.log("Template file saved: ", file.name)
    } else {
      alert("Invalid file type. Please upload a .ppttc file.")
      e.target.value = "";
    }
  }

  function handleKeyFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.ppttc') || fileName.endsWith('.csv')) {
      setKeyFile(file);
      console.log("Key file saved: ", file.name);
    } else {
      alert("Invalid file type. Please upload a .ppttc or .csv file.");
      e.target.value = "";
    }
  }

  function handleSubmit(e) {
    e.preventDefault();

    if (!keyFile || !templateFile) {
      alert("Please upload both files before submitting!");
      return;
    }

    console.log("Submitting Key file: ", keyFile.name);
    console.log("Submitting Template file: ", templateFile.name);
    console.log("Required files successfully submitted");

    setIsUploading(true);
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
          <p>2. PPTX Template</p>
          <input className="choose-file" type="file" name="ppttcFile" accept=".pptx" onChange={ handleTemplateFileChange } />
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
