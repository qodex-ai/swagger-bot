framework_identifier_prompt = """
        You are provided with a list of file names of a repository.
        You need to provide framework for the repo.
        File Names List:
        {file_paths}
        ----
        List of frameworks to choose from:
        {frameworks}
        ----
        Output Format:
        Your output should only be this json and the framework should be one of the framework provided in the list. If the detected framework is not provided in the list choose the similar framework from the provided list.
        {{"framework": ""}}
        """
framework_identifier_system_prompt = "You are a helpful assistant for understanding different framework repositories."

ruby_on_rails_endpoint_extractor_prompt = """You are a Ruby on Rails routing expert. Analyze the provided Rails routes file and return a JSON array of all API endpoints exactly as they would appear in the output of the `rails routes` command.

1. **Accuracy**:
   - The output must include only the endpoints that `rails routes` would display, with exact paths and HTTP methods.
   - Do not generate endpoints that are not explicitly defined or that `rails routes` would not show.
   - Ensure that `new` and `edit` routes are included for all resources, unless they are explicitly excluded using except or restricted using only. If `only` or `except` is specified, include the appropriate API paths accordingly.
   - For nested resources, ensure `new` routes include all parent resource IDs (e.g., `/grandparent/:grandparent_id/parent/:parent_id/name/new`).

2. **JSON Format**:
   - Output must be a JSON array of dictionaries.
   - Each dictionary must have exactly two keys: `method` (uppercase HTTP method, e.g., GET, POST) and `path` (lowercase, starting with `/`, matching the URI pattern from `rails routes`).
   - Example:
     [
       {{"method": "GET", "path": "/api/v1/organisations/:organisation_id/projects/:project_id/collections"}},
       {{"method": "POST", "path": "/api/v1/organisations/:organisation_id/projects/:project_id/collections"}}
     ]
   - Include format suffixes (e.g., `.:format`) only if present in the routes file.

File Content:
{file_content}
"""
ruby_on_rails_endpoint_extractor_system_prompt = "You are an expert Ruby on Rails developer and routing specialist."

golang_endpoint_extractor_system_prompt = "You are an expert `golang` developer and routing specialist."
golang_endpoint_extractor_prompt = """You are a Golang web routing expert. Analyze the provided Go source code and extract all the HTTP API endpoints. Your output must reflect exactly the routes defined in the file without inventing or assuming any missing parts.

1. **Accuracy**:
   - Only include endpoints explicitly defined via standard Go routing patterns (e.g., `http.HandleFunc`, `mux.HandleFunc`, `r.GET`, `router.POST`, `e.GET`, `app.Get`, etc.).
   - Extract the correct HTTP method (e.g., GET, POST, PUT, DELETE, PATCH) and the associated path exactly as defined in the code.
   - If a route uses a path variable (e.g., `"/users/id"` in `mux` or `"/users/:id"` in `gin`), preserve the path syntax exactly as it appears in the code.
   - Do not infer routes not present in the source code.
   - Ignore WebSocket handlers, middleware, or non-HTTP route-related code unless they define a direct HTTP method+path combination.

2. **JSON Format**:
   - Output must be a JSON array of dictionaries.
   - Each dictionary must have exactly two keys: `method` (uppercase HTTP method, e.g., GET, POST) and `path` (lowercase, starting with `/`, matching the path from the source code).
   - Example:
     [
       {{"method": "GET", "path": "/api/v1/users"}},
       {{"method": "POST", "path": "/api/v1/users/:userId/projects"}}
     ]
   - Keep the path parameters (`:id`, etc.) exactly as they appear — do not transform or standardize them across frameworks.

File Content:
{file_content}
"""


express_endpoint_extractor_prompt = """
            You are an Express.js routing expert. Analyze the provided JavaScript file defining Express routes and return a comprehensive and VALID JSON array of all possible endpoints it defines. Ensure the following rules are strictly followed:

            1. **Consistency**:
               - Every output must follow the same format and include all valid endpoints.
               - Missing any valid endpoint or including invalid ones is unacceptable.

            2. **JSON Format**:
               - Output must be a JSON array of dictionaries.
               - Each dictionary should have exactly two keys: "method" and "path".
               - Example:
                 [
                   {{"method": "GET", "path": "/example"}},
                   {{"method": "POST", "path": "/example"}}
                 ]

            3. **Rules for Extraction**:
               a. **Direct Routes**:
                  - Include all HTTP methods (GET, POST, PUT, PATCH, DELETE).
                  - Include routes defined using `app.get`, `app.post`, etc.
                  - Include routes with middleware functions.

               b. **Router Modules**:
                  - Extract routes defined using `express.Router()`.
                  - Ensure paths defined in the parent `app.use('/prefix', router)` are prepended to the router's routes.

               c. **Dynamic and Static Paths**:
                  - Include dynamic parameters (e.g., `/users/:id`).
                  - Include optional parameters (e.g., `/users/:id?`).
                  - Include routes with query parameters explicitly if provided in comments or docs.

               d. **Middlewares**:
                  - Include paths where routes are registered with middleware functions, e.g., `app.use('/api', apiRouter)`.

               e. **Advanced Routes**:
                  - Include nested routers and route chaining.
                  - Include any routes registered via custom methods or libraries.

            4. **Validation**:
               - Ensure every path starts with `/`.
               - Ensure methods are uppercase (GET, POST, etc.).
               - Ensure paths are lowercase.
               - Include all valid HTTP methods.

            Analyze this file:

            {file_content}
            """

express_endpoint_extractor_system_prompt = "You are an expert Express.js developer and routing specialist."
django_endpoint_extractor_prompt = """You are a Django routing expert. Analyze the provided Django urls.py file and return a comprehensive and VALID JSON array of all possible endpoints it defines. Ensure the following rules are strictly followed:

        1. Consistency:
            - Every output must follow the same format and include all valid endpoints.
            - Missing any valid endpoint or including invalid ones is unacceptable.
        2. JSON Format:
            - Output must be a JSON array of dictionaries.
            - Each dictionary should have exactly two keys: "method" and "path".
            Example:
                [
                  {{"method": "GET", "path": "/example/"}},
                  {{"method": "POST", "path": "/example/"}}
                ]
        3. Rules for Extraction:
            a. Direct Routes: - Include all routes explicitly defined in urlpatterns. - Include routes defined using path() and re_path(). - Include routes with named or unnamed URL parameters (e.g., /users/<int:id> or /users/<slug:username>). - Include optional URL parameters if defined (e.g., /users/<int:id>?). - Include routes defined with regex patterns.

            b. View-Based Routes: - Include all valid HTTP methods for routes tied to Django generic views or function-based views (e.g., GET, POST, PUT, PATCH, DELETE). - For class-based views (e.g., APIView, ViewSet), extract all supported methods. - Include routes defined via as_view() and map them to their allowed HTTP methods.

            c. Namespace and Prefixes: - Include all routes under namespaced include() patterns. - Prepend parent path prefixes when analyzing nested routes from included urls.py files.

            d. Dynamic and Static Paths: - Ensure dynamic segments like <int:id> and <str:slug> are represented correctly in the output as /users/:id or /users/:slug. - Include static paths as-is.

            e. Advanced Routes: - Include routes defined with decorators like @api_view and custom method mappings. - Include routes with custom URL converters or constraints.

            f. Django REST Framework (DRF): - For DRF Router instances, extract all routes for registered view sets, including basename and nested routes if any. - Ensure all methods (GET, POST, PUT, PATCH, DELETE) supported by the viewset are included for each route.

        4. Validation:
            - Ensure every path starts with /.
            - Ensure methods are uppercase (GET, POST, etc.).
            - Ensure paths are lowercase and include trailing slashes unless explicitly configured otherwise.
            - Include format suffixes (e.g., .json, .xml) if defined in the routes.

        Analyze this file:

        {file_content}
        """
django_endpoint_extractor_system_prompt= "You are an expert DJANGO developer and routing specialist."
flask_endpoint_extractor_prompt = """
        You are a Flask routing expert. Analyze the provided Python file defining Flask routes and return a comprehensive and VALID JSON array of all possible endpoints it defines. Ensure the following rules are strictly followed:

        1. Consistency:
            Every output must follow the same format and include all valid endpoints.
            Missing any valid endpoint or including invalid ones is unacceptable.
        2. JSON Format:
            Output must be a JSON array of dictionaries.
            Each dictionary should have exactly two keys: "method" and "path".
            Example:
                [
                  {{"method": "GET", "path": "/example/"}},
                  {{"method": "POST", "path": "/example/"}}
                ]

        3. Rules for Extraction:
            a. Direct Routes: - Include all HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS). - Extract routes defined using @app.route or Flask.add_url_rule. - Include dynamic parameters (e.g., /users/<id> or /users/<string:username>). - Include optional parameters (e.g., /users/<id>?).

            b. Blueprints: - Include all routes registered through Blueprint instances. - Prepend the blueprint prefix (if any) to the route paths.

            c. Static and Dynamic Paths: - Ensure dynamic segments like <int:id> and <string:username> are represented as /users/:id or /users/:username. - Include static paths as-is.

            d. Custom Methods: - Include routes registered with custom HTTP methods or method lists. - Account for methods parameters in route decorators.

            e. Middleware and Nested Routes: - Include middleware-wrapped routes. - Account for routes registered with sub-applications or extensions like Flask-RESTful or Flask-Smorest.

            f. API Frameworks: - For Flask-RESTful Api instances, extract all routes and their associated HTTP methods. - For Flask-Smorest or similar frameworks, include paths and methods for registered resources.

        4. Validation:
            - Ensure every path starts with /.
            - Ensure methods are uppercase (GET, POST, etc.).
            - Ensure paths are lowercase and reflect the defined structure.

        Analyze this file:

        {file_content}
"""
flask_endpoint_extractor_system_prompt = "You are an expert Flask developer and routing specialist."

fastapi_endpoint_extractor_prompt = """
                You are a FastAPI routing expert. Analyze the provided Python file defining FastAPI routes and return a comprehensive and VALID JSON array of all possible endpoints it defines. Ensure the following rules are strictly followed:

                1. Consistency:
                    - Every output must follow the same format and include all valid endpoints.
                    - Missing any valid endpoint or including invalid ones is unacceptable.
                2. JSON Format:
                    - Output must be a JSON array of dictionaries.
                    - Each dictionary should have exactly two keys: "method" and "path".
                Example:
                    [
                  {{"method": "GET", "path": "/example/"}},
                  {{"method": "POST", "path": "/example/"}}
                ]
                3. Rules for Extraction:
                    a. Direct Routes: - Include all HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS). - Extract routes defined with @app.get, @app.post, @app.put, etc. - Include routes defined with @app.api_route() and @app.router.

                    b. Dynamic and Static Paths: - Include dynamic parameters (e.g., /items/{{item_id}}) and represent them as /items/:item_id. - Include optional parameters (e.g., /users/{{user_id}}?). - Ensure static paths are included as-is.

                    c. APIRouter: - Include routes defined in APIRouter instances. - Prepend prefixes specified in app.include_router() or APIRouter with the route paths. - Include dependencies or middleware-wrapped routes registered with APIRouter.

                    d. Path Operation Parameters: - Include query parameters explicitly if specified in the Depends() or other parameter definitions.

                    e. Custom Methods: - Account for custom HTTP methods or method lists defined using methods arguments.

                    f. Validation and Serialization: - Extract all routes even if they specify response models, request validation, or dependencies. - Do not modify or skip routes with additional validation logic.

                4. Validation:
                    Ensure every path starts with /.
                    Ensure methods are uppercase (GET, POST, etc.).
                    Ensure paths are lowercase.
                    Include routes with trailing slashes if defined.
                    Include all valid paths from the FastAPI application.

                Analyze this file:
                    {file_content}

    """
fastapi_endpoint_extractor_system_prompt = "You are an expert Fastapi developer and routing specialist."

ruby_on_rails_swagger_generation_prompt = """
            You are an API documentation assistant specializing in Ruby on Rails applications. Generate Swagger (OpenAPI 3.0) JSON for the following Rails endpoint:

            Controller Information: {endpoint_info}
            Method: {endpoint_method}
            Path: {endpoint_path}
            Authentication/Authorization Information: {authentication_information}

            Include:
            1. api_description: A detailed description of the API endpoint's functionality and the parameter limitations.
            2. Expected request parameters (query, path, body) with fully resolved schemas. Do not use $ref or references; include all definitions inline.
            3. Example request and response schemas, fully expanded without references.
            4. Response codes (200, 400, etc.) and their descriptions.
            5. The method in the output should match the Method mentioned above.
            6. Tags should be UpperCamelCase, pluralized, and based on the Rails controller name inferred from the Controller Information.
            7. authorization_tag: This field should be 'Authorization' if the primary function of the endpoint is authentication or authorization (e.g., login, token generation, access management). Otherwise, set it to 'Non-Authorization'. Do not classify it based solely on the presence of an Authorization header.

            Important Notes:
            - If the Controller Information or Authentication/Authorization Information indicates that the endpoint enforces authentication, include the appropriate security scheme in the JSON.
            - If the Controller Information specifies that the endpoint is public or exempt from authentication, do not include a security schema in the JSON.
            - Do not explicitly mention which endpoints require authentication in the instructions. Infer this dynamically based on the provided information.
            - For routes under `sessions` or `registrations` or `users` controllers, omit authentication requirements as these are part of user authentication flows.

            Additional Notes for Rails:
            - Infer parameter names from typical Rails conventions, such as `id` for resource paths or query parameters for filtering, sorting, etc.
            - Include request body schema for JSON payloads, typically used in `create` or `update` actions.
            - Response schemas should match typical Rails patterns, such as objects for `show` or arrays for `index`.

            Sample Output Format:
            ---> {{
            "openapi": "3.0.0",
            "info": {{
                "title": "User Management API",
                "version": "1.0.0"
            }},
            "paths": {{
                "/api/v1/users/{{id}}": {{
                    "get": {{
                        "summary": "Retrieve User Details",
                        "api_description": "Retrieves detailed information about a specific user using the provided ID.",
                        "tags": [
                            "Users"
                        ],
                        "parameters": [
                            {{
                                "name": "id",
                                "in": "path",
                                "required": true,
                                "schema": {{
                                    "type": "string"
                                }},
                                "description": "The unique identifier for the user."
                            }}
                        ],
                        "authorization_tag": "Non-Authorization",
                        "responses": {{
                            "200": {{
                                "description": "User details retrieved successfully.",
                                "content": {{
                                    "application/json": {{
                                        "schema": {{
                                            "type": "object",
                                            "properties": {{
                                                "id": {{
                                                    "type": "string",
                                                    "example": "123"
                                                }},
                                                "name": {{
                                                    "type": "string",
                                                    "example": "John Doe"
                                                }},
                                                "email": {{
                                                    "type": "string",
                                                    "example": "john.doe@example.com"
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }},
                            "404": {{
                                "description": "User not found.",
                                "content": {{
                                    "application/json": {{
                                        "schema": {{
                                            "type": "object",
                                            "properties": {{
                                                "error": {{
                                                    "type": "string",
                                                    "example": "User not found"
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            }}

            Output only valid JSON without any explanations.
        """
generic_swagger_generation_prompt = """
                        You are an API documentation assistant. Generate Swagger (OpenAPI 3.0) JSON for the following endpoint:

                        Method: {endpoint_method}
                        Path: {endpoint_path}
                        Additional Information: {endpoint_info}
                        Authentication/Authorization Information: {authentication_information}

                        Include:
                        1. api_description: A detailed description of the API endpoint's functionality and the parameter limitations.
                        2. Expected request parameters (query, path, body) with fully resolved schemas. Do not use $ref or references; include all definitions inline.
                        3. Example request and response schemas, fully expanded without references.
                        4. Response codes (200, 400, etc.) and their descriptions.
                        5. The method in the output should be same as the Method mentioned above.
                        6. Tags should be UpperCamelCase without space with pluralized form.
                        7. authorization_tag: This field should be 'Authorization' if the primary function of the endpoint is authentication or authorization (e.g., login, token generation, access management). Otherwise, set it to 'Non-Authorization'. Do not classify it based solely on the presence of an Authorization header.


                        **Leverage Authentication/Authorization Information while generating parameters and headers for the endpoint.**

                        Ensure all components are fully expanded and self-contained. Do not include $ref in any part of the output.

                        Sample Output Format:
                        ---> {{
                        "openapi": "3.0.0",
                        "info": {{
                            "title": "User Confirmation API",
                            "version": "1.0.0"
                        }},
                        "paths": {{
                            "/api/v1/users/confirm_email": {{
                                "post": {{
                                    "summary": "Confirm User's Email",
                                    "api_description": "This endpoint confirms a user's email address based on the provided confirmation token.",
                                    "tags": [
                                        "Users"
                                    ],
                                    "requestBody": {{
                                        "required": true,
                                        "content": {{
                                            "application/json": {{
                                                "schema": {{
                                                    "type": "object",
                                                    "properties": {{
                                                        "token": {{
                                                            "type": "string",
                                                            "description": "The confirmation token sent to the user's email."
                                                        }}
                                                    }},
                                                    "required": [
                                                        "token"
                                                    ]
                                                }}
                                            }}
                                        }}
                                    }},
                                    "authorization_tag": "Non-Authorization",
                                    "responses": {{
                                        "200": {{
                                            "description": "Email confirmed successfully",
                                            "content": {{
                                                "application/json": {{
                                                    "schema": {{
                                                        "type": "object",
                                                        "properties": {{
                                                            "message": {{
                                                                "type": "string",
                                                                "example": "Email confirmed successfully"
                                                            }}
                                                        }}
                                                    }}
                                                }}
                                            }}
                                        }},
                                        "422": {{
                                            "description": "Unprocessable Entity",
                                            "content": {{
                                                "application/json": {{
                                                    "schema": {{
                                                        "type": "object",
                                                        "oneOf": [
                                                            {{
                                                                "properties": {{
                                                                    "error": {{
                                                                        "type": "string",
                                                                        "example": "Invalid token"
                                                                    }}
                                                                }}
                                                            }},
                                                            {{
                                                                "properties": {{
                                                                    "error": {{
                                                                        "type": "string",
                                                                        "example": "Token has expired"
                                                                    }}
                                                                }}
                                                            }},
                                                            {{
                                                                "properties": {{
                                                                    "message": {{
                                                                        "type": "string",
                                                                        "example": "Email already confirmed"
                                                                    }}
                                                                }}
                                                            }}
                                                        ]
                                                    }}
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                        }}

                        Output only valid JSON without any explanations.
                """

swagger_generation_system_prompt = "You are a helpful assistant for generating API documentation."