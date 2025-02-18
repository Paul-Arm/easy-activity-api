# EasyActivity API




## Getting Started

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally

Start the development server on http://127.0.0.1:8000

On first time use, install the asgi server [uvicorn](https://www.uvicorn.org/)
```bash
pip install uvicorn
```

run the server via
```bash
uvicorn main:app --reload
```

When you make changes to your project, the server will automatically reload.

## Deploying to Vercel

Deploy your project to Vercel with the following command:

```bash
npm install -g vercel
vercel --prod
```

Or `git push` to this repostory

