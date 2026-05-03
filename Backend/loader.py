from langchain.document_loaders import PyPDFLoader
loader=PyPDFLoader("F:\projects\sheria_AI\Sheria_backend\Backend\EmploymentAct_2007.pdf")#if datais .pdf
docs=loader.load