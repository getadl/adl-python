import simplejson, types, time
from copy import deepcopy
from tornado.web import RequestHandler
from ADL.Utilities import *
from ADL.Utilities.WebUtilities import wu, WebUtilities
from ADL.Service import GraphService
from ADL.WebHarness.QueryResults import QueryResults
from ADL.Operations import Operations

isList = isList
isDict = isDict

operations = Operations()

class MuxDispatcher(WebUtilities, RequestHandler):

	def _return(self, **args): args['response'][args['arg_key']] = deepcopy(args['arg_response']);
	def _aggregate(self, **args): self._aggpipe('aggregate', **args);
	def _pipe(self, **args): self._aggpipe('pipe', **args);

# 	def _map(self, **args):
# 		args_response = deepcopy(args['arg_response'])
# 		mapitems = {}
# 		print '_map: %s' % repr(args)
# 		for key in args['map'].keys():
# # 			print '>>>key: %s' % key
# 			data = QueryResults(args['map'][key], args_response).Items
# 			if not data: continue;
# 			if mapitems.has_key(key): mapitems[key] += data;
# 			else: mapitems[key] = data;
# 		print '_map.mapitems: %s' % repr(mapitems)

	def _aggpipe(self, fx, **args): 
# 		print('_aggpipe.args: %s' % repr(args), True)
		args_response = deepcopy(args['arg_response'])
		
		if fx == 'pipe': dict_key, var_key = ('pipes', args['target']);
		elif fx == 'aggregate': dict_key, var_key = ('response', '_aggregated_');

		if not args[dict_key].has_key(var_key): args[dict_key][var_key] = {};
		target = args[dict_key][var_key];

# 		print 'mapping...: %s' % repr(args['map'])
		for key in args['map'].keys():
# 			print '>>>key: %s' % key
			data = QueryResults(args['map'][key], args_response).Items
			if not data: continue;
# 			if type(data) is not types.ListType: data = [data];
# 			print '_aggpipe(%s).data(%s): %s' % (fx, key, repr(data))
			if target.has_key(key):
				if type(target[key]) is types.StringType: target[key] = [target[key]];
				if type(data) is types.StringType: data = [data];
				target[key] += data;
			else: target[key] = data;

# 		print 'target : %s' % target
		
# 		print 'cleaning...'
		for key in target.keys():
			try:
				if (args['op'] == 'clean' or fx == 'aggregate') and (isList(target[key]) or isTuple(target[key])):
					target[key] = quickCleanList(target[key]);
			except: pass;
# 	 	print 'piped: %s ' % repr(target[key])
			


	def post(self, endpoint): return self.get(endpoint);
	def get(self, endpoint):
		get_t = time.time()
		try:
			print 'MUX.args start %0.3fms' % ((time.time()-get_t)*1000.0)

# 			print('MuxDispatcher.get.endpoint: %s' % repr(endpoint), True)
			args = wu.processRequest(endpoint, self.request.arguments)
			del(args['function'])

# 			print('MuxDispatcher.get.args: %s' % repr(args), True)
			c = GraphService.getContainer(args['user_uuid'], args['graph_uuid'])
			
			response = {}
			pipes = {}

			print 'MUX.args preargs %0.3fms' % ((time.time()-get_t)*1000.0)
			
			mux_args = simplejson.loads(args['args'])
			for	arg in mux_args:
				t1 = time.time()
				try:
# 					print('MUXCALL(%s) -> args: %s' % (arg['key'], repr(arg)), True)
					if not arg.has_key('action_args') or arg['action_args'] is None or not isDict(arg['action_args']): arg['action_args'] = {};

					if arg['object_type'] == 'var':
# 						print 'var.values: %s' % arg['values']
						if not pipes.has_key(arg['target']): pipes[arg['target']] = {};
						pipes[arg['target']].update(arg['values'])
						continue

					if pipes.has_key(arg['key']): arg['action_args'].update(pipes[arg['key']]);
	# 				print '>>action_args: %s' % repr(arg['action_args'])
	
					obj = None
					object_type = arg['object_type']
					if object_type == 'coregraph': 
						obj = c.Graph
					elif object_type == 'operation': 
						obj = operations
					else:
						if object_type == 'plugins': ot = 'Plugins';
						else: ot = 'RefGraphs';
						obj = getattr(getattr(c, ot).Plugins, arg['uuid'], None)
	
					if obj is None: raise Exception('%s doesn\'t exist' % arg['object_type']);

# 					print 'action_args: %s' % arg['action_args']
					arg_response = getattr(obj, arg['action'])(**arg['action_args'])
# 					print 'arg_response: %s' % repr(arg_response)
					
					if isDict(arg['response_action']): arg['response_action'] = [arg['response_action']];
					
# 					print "arg['response_action']: %s" % arg['response_action']
					
					for response_action in arg['response_action']:
						for action in response_action['action'].split('|'):
							try:
								op = None
								if action.find('>') != -1: action, op = action.split('>');
								response_action.update({
									'response' : response,
									'pipes' : pipes,
									'arg_key' : arg['key'],
									'arg_response' : arg_response,
									'op' : op
								})
								getattr(self, '_%s'%action)(**response_action)
		
							except Exception, inst: 
								print('do_arg_actions(%s)' % action, inst);
# 					print 'response: %s' % repr(response)
# 					print 'pipes: %s' % repr(pipes)
# 					print('MUXCALL(%s) -> DONE' % arg['key'], True)
				except Exception, inst:
					response[arg['key']] = {
						'status' : 'error',
						'msg' : inst.args[0]
					}
				print 'MUXCALL.%s took %0.3fms' % (arg['key'], (time.time()-t1)*1000.0)
# 
# 			print ''
# 			print 'response: %s' % repr(response)
# 			print 'pipes: %s' % repr(pipes)
			print 'MUX.args preresponse %0.3fms' % ((time.time()-get_t)*1000.0)
			self.doResponse(True, {'response' : response})

		except Exception, inst: self.doResponse(False, inst.args[0])
		print 'MUX.args took %0.3fms' % ((time.time()-get_t)*1000.0)
