from sisvitapp import initflask



app = initflask.create_app()


if __name__=='__main__' : 
    app.run(port=5432)