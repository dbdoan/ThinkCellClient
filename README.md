# ThinkCellClient

# Preview
<img src="https://i.ibb.co/HLnvmBqP/think-Cell-Automator-Preview.jpg" alt="Preview of Thinkcell Automator website" width="auto" height="auto">

## About

A web application that converts CSV (Excel) data into Think-Cell PowerPoint presentations using a predefined template, streamlining the creation of consistent and data-driven slides.

## How-to
Pre-Req: Set-up an environment with FASTAPI and React.
1. Create a .env file in the FastAPI folder with VITE_LOCAL_URL, VITE_EXTERNAL_URL, FASTAPI_EXTERNAL_URL, THINKCELL_SERVER_URL set.
2. Create a .env file under Thinkcell-Panel folder with VITE_FASTAPI_ENDPOINT set.
3. Start Think-cell Server with Think-cell's included server program on a Windows machine.
4. Start FASTAPI and React site.
5. To test, I have included sample files from Think-cell themselves, under FastAPI folder. JSON formatted PTTCC and PPTX template.

## Roadmap

# Backend
- [x] Complete core csv to pptx conversion
- [x] Create API to accept input files
- [x] Thinkcell Server to FastAPI integration
- [x] PPTTC + PPTX => PPTX logic
- [x] Moved Think-cell server hosting to Azure 24/7

# Frontend
- [ ] Add box for access code
- [x] Revert in-progress submit btn back to submit after processed
- [ ] Error handling appearance
- [x] Reset chosen files

# Low Priority
- [ ] POSTGRE SQL server to store access codes
- [ ] Access code generation validation
