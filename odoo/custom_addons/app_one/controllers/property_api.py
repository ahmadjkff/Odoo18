import json
from pickle import FALSE
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request

def valid_response(data, status):
    response_body = {
        'data':data,
    }
    return request.make_json_response(response_body,status=status)

def invalid_response(error,status):
    response = {
        'error':error
    }
    return request.make_json_response(response,status=status)

class PropertyApi(http.Controller):

    @http.route("/v1/property",methods=["POST"],type="http", auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            request.env['property'].sudo().create(vals)
            if not vals.get('name'):
                return {'message': 'name is required'}
            return valid_response({"message": f"Property '{vals.get('name', 'Unknown')}' created successfully"},status=201)
        except Exception as e:
            return invalid_response({
                "error": "Failed to create property",
                "details": str(e)
            }, 400)

    @http.route("/v1/property/json",methods=["POST"],type="json",auth="none",csrf=False)
    def post_property_json(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            request.env['property'].sudo().create(vals)
            if not vals.get('name'):
                return {'message': 'name is required'}
            return {"message": f"Property '{vals.get('name', 'Unknown')}' created successfully (json)"}
        except Exception as e:
            return {
                "error": "Failed to create property (json)",
                "details": str(e)
            }

    @http.route('/v1/property/<int:property_id>', methods=["PUT"], type='http', auth='none', csrf=False)
    def put_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=',property_id)])
            if not property_id:
                return invalid_response({'error':'property with this id does not exist'},400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)

            return valid_response({'message': 'property has been updated successfully'},200)

        except Exception as e:
            return invalid_response({'error': e},400)

    @http.route('/v1/property/<int:property_id>', methods=["GET"], type='http',auth='none', csrf= False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response({'error':'property with this id does not exist'},400)
            return valid_response({
                'id': property_id.id,
                'name': property_id.name,
                'ref': property_id.ref,
                'bedrooms': property_id.bedrooms
            },200)
        except Exception as error:
            return invalid_response({'error':error},400)

    @http.route('/v1/property/<int:property_id>', methods=["DELETE"],type='http',auth='none',csrf=False)
    def delete_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response({'error':'property with this id does not exist'},400)
            property_id.unlink()
            return valid_response({'message':'Property has been deleted successfully'},status=200)
        except Exception as error:
            return invalid_response({'error':error},400)

    @http.route('/v1/properties', methods=["GET"], type='http', auth='none', csrf=False)
    def get_property_list(self):
        try:
            property_domain = [] # filtration purposes
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain)
            if not property_ids:
                return invalid_response({'error': 'there are no records'}, 400)
            return valid_response([{
                'id': property_id.id,
                'name': property_id.name,
                'ref': property_id.ref,
                'bedrooms': property_id.bedrooms
            } for property_id in property_ids],200 )
        except Exception as error:
            return invalid_response({'error': error}, 400)