from flask import Flask, request, abort, jsonify 
from flask_cors import CORS
from models import setup_db, Book, db

BOOKS_PER_SHELF = 8


# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.app_context().push()

   # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS, PATCH"
        )
        return response
    

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to add a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route("/books", methods=["POST"])
    def create_book():
        page = request.args.get("page", 1, type=int)
        new_title = request.get_json()["title"]
        new_author = request.get_json()["author"]
        new_rating = request.get_json()["rating"]

        if request.method == "POST":
            book = Book(title=new_title, author=new_author, rating=new_rating)
            book.insert()
            current_books = Book.query.order_by(Book.id).paginate(page=page, per_page=BOOKS_PER_SHELF, error_out=False)
            return jsonify({
                "success": True,
                "created": book.id,
                "books": [book.format() for book in current_books],
                "total_books": len(Book.query.all())
            })
        elif request.method != "POST":
            abort(405)
        else:
            abort(404)

        
    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
   
    #def get_books():
    @app.route("/books")
    @app.route("/")
    def get_books():
        page = request.args.get("page", 1, type=int)
        error = False
        try:
            current_books = Book.query.order_by(Book.id).paginate(page=page, per_page=BOOKS_PER_SHELF, error_out=False)
            if current_books is None:
                abort(404)
            else:
                return jsonify({
                        "success": True,
                        "books": [book.format() for book in current_books],
                        "total_books": len(Book.query.all()),
                    })
        except:
           error =True
           db.sessio.rollback()
           if error:
               abort(404)
        finally:
            db.session.close()
            
    # A route that returns a specific book
    @app.route("/books/<int:book_id>")
    def get_specific_book(book_id):
        book = Book.query.get(book_id)
        if book is None:
            abort(404)
        else: 
            return jsonify({
                "success": True,
                "book_id": book.id,
                "book_title":book.title,
                "book_rating":book.rating,
                "book_author":book.author
            })
        
        

    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route("/books/<int:book_id>", methods=["PATCH", "POST"])
    def update_book(book_id):
        body = request.get_json()
        book = Book.query.get(book_id)
        if book is None:
            abort(404)
        rating = int(body.get("rating"))
        book.rating = rating
        book.update()
        return jsonify({
            "success":True,
            "book_id":book.id,
            "updated_rating":book.rating
        })
            
           
    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    #@copy_current_request_context
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)
            else:
                book.delete() 
            books_remaining = Book.query.all()
            return jsonify({
                "success": True,
                "deleted_book_id": book_id,
                "books_remaining": [book.format() for book in books_remaining],
                "total_books_remaining": len(books_remaining)
            })
        except:
            abort(404)
        

    # @TODO: Review the above code for route handlers.
    #        Pay special attention to the status codes used in the aborts since those are relevant for this task!

    # @TODO: Write error handler decorators to handle AT LEAST status codes 400, 404, and 422.

    # TEST: Practice writing curl requests. Write some requests that you know will error in expected ways.
    #       Make sure they are returning as expected. Do the same for other misformatted requests or requests missing data.
    #       If you find any error responses returning as HTML, write new error handlers for them.
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success': False,
            'error_code': 400,
            'error_message':'Bad Request'
        }), 400)

    @app.errorhandler(404)
    def resource_not_found(error):
        return (jsonify({
            'success': False,
            'error_code': 404,
            'error_message':'Resource not found'
        }), 404)
    
    @app.errorhandler(405)
    def unallowed_method(error):
        return (jsonify({
            'success': False,
            'error_code': 405,
            'error_message':'Method not allowed'
        }), 405)
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False,
            'error_code': 422,
            'error_message':'Request not processable'
        }), 422)

    return app
    
