# POWDER Portal API probe

- Checked UTC: 2026-08-24T17:05:41Z
- WellPulse SHA: b2b23629f5c8afd6374857f7d48394762bf191b3
- Source: official emulab/portal-api repository
- Credentials used: **NONE**
- Resource action attempted: **NONE**

## Repository top level
```text
.git/HEAD
.git/config
.git/description
.git/index
.git/packed-refs
.git/shallow
.gitignore
.gitlab-ci.yml
README.md
build.sh
cloudlabclient/__init__.py
docker/Dockerfile
docker/Dockerfile.builder
docker/Dockerfile.installer
openapi.json
portal_api.egg-info/PKG-INFO
portal_api.egg-info/SOURCES.txt
portal_api.egg-info/dependency_links.txt
portal_api.egg-info/entry_points.txt
portal_api.egg-info/requires.txt
portal_api.egg-info/scm_file_list.json
portal_api.egg-info/scm_version.json
portal_api.egg-info/top_level.txt
pyproject.toml
```

## README command/auth excerpts
```text
1:# portal-api (Cloudlab/Powder Python 3 API client library and CLI tools)
2-
3:This repository contains a Python 3 API client library based on API
4-bindings (models and API function wrappers) automatically generated
5-from the `openapi.json` file in this repository. Bindings are generated using
6:[our fork](https://gitlab.flux.utah.edu/openzms/openapi-python-client) of
7:`openapi-python-client`, which has additional support for some of the
8-`openapi` extension attributes we provide to help generators create better
9-code.
10-
11-This repository also provides a [`typer`](https://typer.tiangolo.com/)-based
12:dynamically-generated CLI tool.  On invocation, the CLI tool scans a subset
13-of the generated API function wrappers and uses a combination of `typer` and
14:`click` to wrap them into a CLI tool that exposes each API endpoint as a
15-subcommand.
16-
17-Auto generated API documentation is available at
18-http://emulab.pages.flux.utah.edu/portal-api, most of the examples
19:below are included there, on the right hand side. Look for the `CLI`
20-and `Python` tabs in the `Request Samples` section of each endpoint.
21-
22-The full usage manual for Cloudlab is at https://docs.cloudlab.us/ and
--
24-rest of this document will make more sense if you read one of those
25-first.
26-
27:## Installing from source
28-
29:Most likely you will want to install this library and its tools with
30:`virtualenv` (drop the `'[cli]'` if you don't require the CLI):
31-
32-```
33-python -m venv path/to/your/venv
34-. path/to/your/venv/bin/activate
35:pip install .'[cli]'
36-```
37-
38:Then you can run `portal-cli --help`, or use the library.  Leave the
39-`virtualenv` via `deactivate`. 
40-
41:You can also install locally with `pip`:
42-
43-```
44:pip install --user .'[cli]'
45-```
46-
47-## Using the Portal API
48-
49:In order to use the Portal API, you need to download a `token` from
50:the Cloudlab (or Powder) web UI. After you log in, click on your name
51:in the upper right and select `Portal API Token`. A token will be
52:downloaded to your desktop. At the moment you can have only one token,
53-which is valid for two months. Eventually this will change to allow
54:longer tokens and token refresh. But for now you will need to download
55:a new token periodically.
56-
57:Your token is not encrypted and does not require a password to use.
58:You should never store your token in a public repository!
59-
60:Once you have your token and are ready to use it, the easiest thing
61-to do is export it as an environment variable, along with the URL of
62-the server. 
63-
64:	export PORTAL_TOKEN="your_token_string"
65-	export PORTAL_HTTP="https://boss.emulab.net:43794"
66-
67:You can also pass the token and url via command line arguments.
68-
69:	portal-api --token "your_token_string" --portal-url "https://..." ...
70-
71:For example, to get a list of your experiments:
72-
73:	mypc> portal-api experiment list
74-	[
75-        {
76-            "created_at": "2025-02-19T14:19:16+00:00",
--
78-            "expires_at": null,
79-            "group": null,
80-            "id": "7ce46d72-eecc-11ef-af1a-e4434b2381fc",
81:            "last_snapshot_status": null,
82-            "name": "lbs-frontend",
83:            "profile_id": "7f0cfde3-cf91-11ef-828b-e4434b2381fc",
84:            "profile_name": "small-lan",
85:            "profile_project": "emulab-ops",
86:            "project": "testbed",
87-            "started_at": "2025-02-19T14:19:19+00:00",
88:            "status": "ready",
89-            "expires_at": "2025-02-20T06:00:00+00:00",
90-            "aggregates": {
91:                "urn:publicid:IDN+emulab.net+authority+cm": {
92-                    "name": null,
93-                    "nodes": [
94-                        {
95:                            "client_id": "node0",
96-                            "rawstate": "ISUP",
97:                            "startup_status": null,
98-                            "state": "started",
99:                            "status": "ready",
100:                            "urn": "urn:publicid:IDN+emulab.net+authority+cm"
101-                        }
102-                    ],
103:                    "status": "ready",
104:                    "urn": "urn:publicid:IDN+emulab.net+authority+cm"
105-                }
106-            },
107-        }
--
109-
110-And a fragment of python code that does the same:
111-
112:	from cloudlabclient.portal.client import PortalClient
113:	from cloudlabclient.portal.v1.models import ExperimentList
114-
115:	Portal = PortalClient("https://boss.emulab.net:43794",
116:                          "your_token_string",
117:                          detailed=False, raise_on_unexpected_status=True)
118-	
119:	explist = Portal.list_experiments()
120:	print(str(explist.experiments))
121-
122-
123:## Experiments
124-
125-The following sections include examples of various operations. Only
126-some will include a python version, the rest can be gleaned from the
--
128-http://emulab.pages.flux.utah.edu/portal-api
129-
130-Several of the examples reference files that are contained in the
131:`cloudlabclient/tests` directory of this repository. 
132-
133:### Creating an experiment
134-
135:For this example, we are using the `small-lan` profile, which is a
136:parameterized profile that requires a set of binding variables. The
137-bindings are provided as a json object, and while you can do that
138-on the command line, it is easier to put them in a file and provide
139-the filename on the command line, prefaced with an `@` sign. Here
140:are the bindings we are going to use to instantiate a 1 node
141:experiment at the Emulab cluster:
142-
143-	{
144-		"nodeCount": "1",
--
147-	}
148-
149-Which are stored in a file in this repository. The command line to
150:start this experiment, and have it terminate in one hour:
151-	
152:	EXPID=`portal-cli experiment create --name apitest --project myproject \
153:		--profile-name small-lan --profile-project PortalProfiles --duration 1 \
154:		--bindings @cloudlabclient/tests/experiments/bindings-1node.json | jq -r .id`
155-	export EXPID
156-	
157-EXPID is needed for the couple of examples. A python fragment to do
158-the same:
159-
160:	from cloudlabclient.portal.client import PortalClient
161:	from cloudlabclient.portal.v1.models import ExperimentCreate, AnyObject
162-
163:	Portal = PortalClient("https://boss.emulab.net:43794",
164:						  "your_token_string",
165:						  detailed=False, raise_on_unexpected_status=True)
166-
167:	myexp = Portal.create_experiment(body = ExperimentCreate(
168-		name = "apitest",
169:		project = "testbed",
170-		duration = 1,
171:		profile_name = "small-lan",
172:		profile_project = "PortalProfiles",
173-		bindings = AnyObject.from_dict({
174-			"nodeCount": "1",
175-			"phystype": "d710",
--
177-		})
178-	))
179-
180:### Getting experiment status
181-
182:To get the experiment status you need the experiment ID (from
183-above). The return value is the same as the return value from
184:`create_experiment` and has been slightly abbreviated:
185-
186:	portal-cli experiment get --experiment-id $EXPID
187-	{
188-		"aggregates": {
189:			"urn:publicid:IDN+emulab.net+authority+cm": {
190-				"nodes": [
191-					{
192:						"client_id": "node0",
193-						"rawstate": "ISUP",
194:						"startup_status": null,
195-						"state": "started",
196:						"status": "ready",
197:						"urn": "urn:publicid:IDN+emulab.net+authority+cm"
198-					}
199-				],
200:				"status": "ready",
201:				"urn": "urn:publicid:IDN+emulab.net+authority+cm"
202-			}
203-		},
204-		"bindings": {
--
211-		"creator": "stoller",
212-		"id": "e0174522-6bdc-11f0-bc80-e4434b2381fc",
213-		"name": "apitest",
214:		"profile_id": "33e0df61-0f4d-11f0-828b-e4434b2381fc",
215:		"profile_name": "small-lan",
216:		"profile_project": "PortalProfiles",
217:		"project": "testbed",
218:		"status": "ready",
219-	}
220-	
221:### Modify an experiment.
222-
223:Experiments that are instantiated from `parameterized profiles` can be
224-modified when they are in the `ready` state. Modification is done by 
225-providing a new set of bindings, different then the original bindings
226:that were supplied when creating the experiment. Using the one node
227-example above, this set of bindings will add another node:
228-
229-	{
--
233-	}
234-
235-These bindings are also stored in a file in this repository. The
236:command line to start the experiment modification is:
237-
238:	portal-cli experiment modify --experiment-id $EXPID \
239:		--bindings @cloudlabclient/tests/experiments/bindings-2node.json
240-	
241:### Getting experiment manifests
242-
243:Once the experiment is ready, you can ask for the manifests(s):
244-
245:	portal-cli experiment manifests get --experiment-id $EXPID
246-
247-This will return a dictionary keyed by the aggregate (cluster)
248-URNs. The value is a string which will need to be XML decoded.
249-
250:### Terminating an experiment
251-
252:	portal-cli experiment terminate --experiment-id $EXPID
253-	
254-After a little while:
255-
256:	portal-cli experiment get --experiment-id $EXPID
257-	{
258-		"code": 404,
259:		"error": "No such experiment",
260-	}
261-
262:### Extending an experiment
263-
264:Experiments can be extended in hour units. In general, the first week
265-or two will be granted automatically. Beyond that, an administrator
266-will need to approve the request. If the extension request is
267-immediately rejected, an error value will be returned. If your request
268-requires administrator intervention, you will receive email when it is
269:approved (or rejected). The return value is the new experiment status,
270-you can use the new value of `expires_at` to determine how much
271-time was granted.
272-
273:	portal-cli experiment extend --experiment-id $EXPID --extend-by 2
274-	
275-Instead of `extend-by` you can supply an absolute GMT timestamp:
276-
277:	portal-cli experiment extend --experiment-id $EXPID --expires-at "2025-07-28T19:01:30+00:00"
278-
279-You may optionally supply a `--reason` option to provide a pithy yet
280-informative reason for your extension. This is sometimes helpful when
281-your request requires administrator approval and the Portal is very
282-busy. If you are working on a near deadline, be sure to mention that.
283-	
284:	portal-cli experiment extend --experiment-id $EXPID --extend-by 2
285-	--reason @/tmp/reason.txt
286-	
287:### Reboot/reload/powercycle/stop/start nodes in an experiment
288-
```

## CLI help — root
```text
[1m                                                                                [0m
[1m [0m[1;33mUsage: [0m[1mportal-cli [OPTIONS] COMMAND [ARGS]...[0m[1m                                 [0m[1m [0m
[1m                                                                                [0m
 An Portal client.                                                              
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [1;36m-[0m[1;36m-debug[0m              [1;35m-[0m[1;35m-no[0m[1;35m-debug[0m          [1;33m                [0m  Print debugging   [2m│[0m
[2m│[0m                                                            info from         [2m│[0m
[2m│[0m                                                            `client` modules. [2m│[0m
[2m│[0m                                                            [2;33m[env var:        [0m [2m│[0m
[2m│[0m                                                            [2;33mCLIENT_DEBUG]    [0m [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-debug]        [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-debug[0m[1;36m-all[0m          [1;35m-[0m[1;35m-no[0m[1;35m-debug-all[0m      [1;33m                [0m  Print debugging   [2m│[0m
[2m│[0m                                                            from Python root  [2m│[0m
[2m│[0m                                                            logger            [2m│[0m
[2m│[0m                                                            (everything).     [2m│[0m
[2m│[0m                                                            [2;33m[env var:        [0m [2m│[0m
[2m│[0m                                                            [2;33mCLIENT_DEBUG_ALL][0m [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-debug-all]    [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-include[0m[1;36m-raw[0m        [1;35m-[0m[1;35m-no[0m[1;35m-include-raw[0m    [1;33m                [0m  Include *_raw     [2m│[0m
[2m│[0m                                                            subcommands for   [2m│[0m
[2m│[0m                                                            create/update     [2m│[0m
[2m│[0m                                                            calls that        [2m│[0m
[2m│[0m                                                            require a JSON    [2m│[0m
[2m│[0m                                                            object, in        [2m│[0m
[2m│[0m                                                            addition to their [2m│[0m
[2m│[0m                                                            'exploded' forms. [2m│[0m
[2m│[0m                                                            [2;33m[env var:        [0m [2m│[0m
[2m│[0m                                                            [2;33mCLIENT_INCLUDE_R…[0m [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-include-raw]  [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-token[0m                                  [1;33mTEXT            [0m  Portal API token  [2m│[0m
[2m│[0m                                                            for               [2m│[0m
[2m│[0m                                                            authentication.   [2m│[0m
[2m│[0m                                                            [2;33m[env var:        [0m [2m│[0m
[2m│[0m                                                            [2;33mPORTAL_TOKEN]    [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-portal[0m[1;36m-url[0m                             [1;33mTEXT            [0m  Portal service    [2m│[0m
[2m│[0m                                                            URL (excluding    [2m│[0m
[2m│[0m                                                            version).         [2m│[0m
[2m│[0m                                                            [2;33m[env var:        [0m [2m│[0m
[2m│[0m                                                            [2;33mPORTAL_HTTP]     [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-elaborate[0m          [1;35m-[0m[1;35m-no[0m[1;35m-elaborate[0m      [1;33m                [0m  Return elaborated [2m│[0m
[2m│[0m                                                            objects with      [2m│[0m
[2m│[0m                                                            foreign key child [2m│[0m
[2m│[0m                                                            relationships.    [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-elaborate]    [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-error[0m[1;36m-detail[0m       [1;35m-[0m[1;35m-no[0m[1;35m-error-deta…[0m    [1;33m                [0m  Show detailed     [2m│[0m
[2m│[0m                                                            error information [2m│[0m
[2m│[0m                                                            on exception.     [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-error-detail] [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-force[0m              [1;35m-[0m[1;35m-no[0m[1;35m-force[0m          [1;33m                [0m  Force update or   [2m│[0m
[2m│[0m                                                            deletion even if  [2m│[0m
[2m│[0m                                                            dependent         [2m│[0m
[2m│[0m                                                            resources exist.  [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mno-force]        [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-timeout[0m                                [1;33mFLOAT           [0m  Timeout for HTTP  [2m│[0m
[2m│[0m                                                            requests.         [2m│[0m
[2m│[0m                                                            [2m[default: 30.0]  [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-follow[0m[1;36m-redirec…[0m    [1;35m-[0m[1;35m-no[0m[1;35m-follow-red…[0m    [1;33m                [0m  Follow HTTP       [2m│[0m
[2m│[0m                                                            redirects.        [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mfollow-redirects][0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-raise[0m[1;36m-on-unexp…[0m    [1;35m-[0m[1;35m-no[0m[1;35m-raise-on-u…[0m    [1;33m                [0m  Raise an error on [2m│[0m
[2m│[0m                                                            unexpected HTTP   [2m│[0m
[2m│[0m                                                            return status.    [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mraise-on-unexpec…[0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-raise[0m[1;36m-on-undec…[0m    [1;35m-[0m[1;35m-no[0m[1;35m-raise-on-u…[0m    [1;33m                [0m  Raise an error on [2m│[0m
[2m│[0m                                                            undecodable HTTP  [2m│[0m
[2m│[0m                                                            return content.   [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mraise-on-undecod…[0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-verify[0m[1;36m-ssl[0m         [1;35m-[0m[1;35m-no[0m[1;35m-verify-ssl[0m     [1;33m                [0m  Enable SSL        [2m│[0m
[2m│[0m                                                            verification      [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2mverify-ssl]      [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-output[0m                                 [1;2;33m[[0m[1;33mjson[0m[1;2;33m|[0m[1;33mraw[0m[1;2;33m|[0m[1;33mpretty[0m  Output format.    [2m│[0m
[2m│[0m                                          [1;2;33m][0m[1;33m               [0m  [2m[default: json][0m   [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-output[0m[1;36m-pretty-…[0m    [1;35m-[0m[1;35m-no[0m[1;35m-output-pre…[0m    [1;33m                [0m  Recursively print [2m│[0m
[2m│[0m                                                            related objects.  [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2moutput-pretty-re…[0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-output[0m[1;36m-pretty-…[0m                        [1;33mINTEGER         [0m  Max char width to [2m│[0m
[2m│[0m                                                            print (with       [2m│[0m
[2m│[0m                                                            exceptions: we    [2m│[0m
[2m│[0m                                                            will never        [2m│[0m
[2m│[0m                                                            truncate field    [2m│[0m
[2m│[0m                                                            names or record   [2m│[0m
[2m│[0m                                                            type titles; and  [2m│[0m
[2m│[0m                                                            we will never     [2m│[0m
[2m│[0m                                                            truncate values   [2m│[0m
[2m│[0m                                                            below 5           [2m│[0m
[2m│[0m                                                            characters).      [2m│[0m
[2m│[0m                                                            Defaults to the   [2m│[0m
[2m│[0m                                                            width of your     [2m│[0m
[2m│[0m                                                            terminal if we    [2m│[0m
[2m│[0m                                                            can extract it    [2m│[0m
[2m│[0m                                                            (>=Python 3.3),   [2m│[0m
[2m│[0m                                                            else 80           [2m│[0m
[2m│[0m                                                            characters.       [2m│[0m
[2m│[0m                                                            [2m[default: 80]    [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-output[0m[1;36m-pretty-…[0m                        [1;33mINTEGER         [0m  Indentation level [2m│[0m
[2m│[0m                                                            for related       [2m│[0m
[2m│[0m                                                            objects.          [2m│[0m
[2m│[0m                                                            [2m[default: 2]     [0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-output[0m[1;36m-pretty-…[0m    [1;35m-[0m[1;35m-no[0m[1;35m-output-pre…[0m    [1;33m                [0m  Pretty-print      [2m│[0m
[2m│[0m                                                            datetimes in      [2m│[0m
[2m│[0m                                                            local timezone.   [2m│[0m
[2m│[0m                                                            [2m[default:        [0m [2m│[0m
[2m│[0m                                                            [2moutput-pretty-lo…[0m [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-install[0m[1;36m-comple…[0m                        [1;33m                [0m  Install           [2m│[0m
[2m│[0m                                                            completion for    [2m│[0m
[2m│[0m                                                            the current       [2m│[0m
[2m│[0m                                                            shell.            [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-show[0m[1;36m-completion[0m                        [1;33m                [0m  Show completion   [2m│[0m
[2m│[0m                                                            for the current   [2m│[0m
[2m│[0m                                                            shell, to copy it [2m│[0m
[2m│[0m                                                            or customize the  [2m│[0m
[2m│[0m                                                            installation.     [2m│[0m
[2m│[0m [1;36m-[0m[1;36m-help[0m                                   [1;33m                [0m  Show this message [2m│[0m
[2m│[0m                                                            and exit.         [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m
[2m╭─[0m[2m Commands [0m[2m──────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [1;36mexperiment [0m[1;36m [0m                                                                 [2m│[0m
[2m│[0m [1;36mprofile    [0m[1;36m [0m                                                                 [2m│[0m
[2m│[0m [1;36mresgroup   [0m[1;36m [0m                                                                 [2m│[0m
[2m│[0m [1;36mtoken      [0m[1;36m [0m                                                                 [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## CLI help — profile
```text
[1m                                                                                [0m
[1m [0m[1;33mUsage: [0m[1mportal-cli profile [OPTIONS] COMMAND [ARGS]...[0m[1m                         [0m[1m [0m
[1m                                                                                [0m
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [1;36m-[0m[1;36m-help[0m          Show this message and exit.                                  [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m
[2m╭─[0m[2m Commands [0m[2m──────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [1;36mcreate     [0m[1;36m [0m                                                                 [2m│[0m
[2m│[0m [1;36mcreate_raw [0m[1;36m [0m Create a new profile                                            [2m│[0m
[2m│[0m [1;36mdelete     [0m[1;36m [0m Delete a profile                                                [2m│[0m
[2m│[0m [1;36mget        [0m[1;36m [0m Retrieve a specific profile                                     [2m│[0m
[2m│[0m [1;36mlist       [0m[1;36m [0m Get profile list                                                [2m│[0m
[2m│[0m [1;36mmodify     [0m[1;36m [0m                                                                 [2m│[0m
[2m│[0m [1;36mmodify_raw [0m[1;36m [0m Modify a profile                                                [2m│[0m
[2m│[0m [1;36mupdate     [0m[1;36m [0m Trigger an update on a repository backed profile                [2m│[0m
[2m│[0m [1;36mversion    [0m[1;36m [0m                                                                 [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## CLI help — profile get
```text
[1m                                                                                [0m
[1m [0m[1;33mUsage: [0m[1mportal-cli profile get [OPTIONS][0m[1m                                       [0m[1m [0m
[1m                                                                                [0m
 Retrieve a specific profile                                                    
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-profile[0m[1;36m-id[0m        [1;33mTEXT[0m  The target experiment ID. [2;31m[required][0m            [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-help[0m              [1;33m    [0m  Show this message and exit.                     [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## CLI help — experiment create
```text
[1m                                                                                [0m
[1m [0m[1;33mUsage: [0m[1mportal-cli experiment create [OPTIONS][0m[1m                                 [0m[1m [0m
[1m                                                                                [0m
 Create a cloudlab experiment.                                                  
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-name[0m                   [1;33mTEXT                  [0m  A human readable name    [2m│[0m
[2m│[0m                                                     for the experiment       [2m│[0m
[2m│[0m                                                     [2;31m[required]              [0m [2m│[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-project[0m                [1;33mTEXT                  [0m  The project the          [2m│[0m
[2m│[0m                                                     experiment is            [2m│[0m
[2m│[0m                                                     instantiated in.         [2m│[0m
[2m│[0m                                                     [2;31m[required]              [0m [2m│[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-profile[0m[1;36m-name[0m           [1;33mTEXT                  [0m  The name of the profile. [2m│[0m
[2m│[0m                                                     [2;31m[required]              [0m [2m│[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-profile[0m[1;36m-project[0m        [1;33mTEXT                  [0m  The name of the profile  [2m│[0m
[2m│[0m                                                     project                  [2m│[0m
[2m│[0m                                                     [2;31m[required]              [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-group[0m                  [1;33mSTR                   [0m  The project subgroup the [2m│[0m
[2m│[0m                                                     experiment is            [2m│[0m
[2m│[0m                                                     instantiated in.         [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-start[0m[1;36m-at[0m               [1;2;33m[[0m[1;33m%Y-%m-%dT%H:%M:%S%z[0m[1;2;33m|[0m[1;33m%[0m  Schedule experiment to   [2m│[0m
[2m│[0m                             [1;33mY-%m-%dT%H:%M:%S.%f%z[0m[1;2;33m|[0m  start at a future time   [2m│[0m
[2m│[0m                             [1;33m%Y-%m-%d[0m[1;2;33m|[0m[1;33m%Y-%m-%dT%H:%[0m  [2m[default: Unset]        [0m [2m│[0m
[2m│[0m                             [1;33mM:%S[0m[1;2;33m|[0m[1;33m%Y-%m-%d         [0m                           [2m│[0m
[2m│[0m                             [1;33m%H:%M:%S[0m[1;2;33m][0m[1;33m             [0m                           [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-stop[0m[1;36m-at[0m                [1;2;33m[[0m[1;33m%Y-%m-%dT%H:%M:%S%z[0m[1;2;33m|[0m[1;33m%[0m  Schedule experiment to   [2m│[0m
[2m│[0m                             [1;33mY-%m-%dT%H:%M:%S.%f%z[0m[1;2;33m|[0m  stop at a future time    [2m│[0m
[2m│[0m                             [1;33m%Y-%m-%d[0m[1;2;33m|[0m[1;33m%Y-%m-%dT%H:%[0m  [2m[default: Unset]        [0m [2m│[0m
[2m│[0m                             [1;33mM:%S[0m[1;2;33m|[0m[1;33m%Y-%m-%d         [0m                           [2m│[0m
[2m│[0m                             [1;33m%H:%M:%S[0m[1;2;33m][0m[1;33m             [0m                           [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-duration[0m               [1;33mINT                   [0m  Initial experiment       [2m│[0m
[2m│[0m                                                     duration in hours        [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-paramset[0m[1;36m-name[0m          [1;33mSTR                   [0m  Optional name of a       [2m│[0m
[2m│[0m                                                     parameter set to apply   [2m│[0m
[2m│[0m                                                     to the profile           [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-paramset[0m[1;36m-owner[0m         [1;33mSTR                   [0m  The owner of the         [2m│[0m
[2m│[0m                                                     parameter set            [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-bindings[0m               [1;33mANYOBJECT             [0m  [2m[default: Unset][0m         [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-refspec[0m                [1;33mSTR                   [0m  For a repository based   [2m│[0m
[2m│[0m                                                     profile, optionally      [2m│[0m
[2m│[0m                                                     specify a refspec[:hash] [2m│[0m
[2m│[0m                                                     to use instead of the    [2m│[0m
[2m│[0m                                                     HEAD of the default      [2m│[0m
[2m│[0m                                                     branch                   [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-sshpubkey[0m              [1;33mSTR                   [0m  Additional ssh public    [2m│[0m
[2m│[0m                                                     key for the experiment.  [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-help[0m                   [1;33m                      [0m  Show this message and    [2m│[0m
[2m│[0m                                                     exit.                    [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## Python/package metadata
```text
[build-system]
requires = [
    "setuptools>=61",
    "setuptools_scm>=7",
    "attrs>=21.3.0",
    "typer<0.26.0",
    "lxml",
    "build",
    "wheel",
]
build-backend = "setuptools.build_meta"

[project]
name = "portal-api"
authors = [
    { name = "Leigh Stoller", email = "stoller@flux.utah.edu" },
    { name = "David M. Johnson", email = "johnsond@flux.utah.edu" },
]
description = "Provides an Portal Python 3 API client library and CLI tool."
keywords = [
    "CloudLab",
    "Powder"
]
requires-python = ">=3.8"
dynamic = [
    "version",
    "readme",
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries"
]

dependencies = [
    "httpx>=0.20.0,<0.28.0",
    "attrs>=21.3.0",
    "python-dateutil>=2.8.0",
    "websockets>=10",
    "typing_extensions",
    "lxml",
]

[project.optional-dependencies]
cli = [
    "typer<0.26.0",
    "lxml",
    "click<8.2.0",
    "griffe>=0.40"
]
bindings = [
    "openapi-python-client @ git+https://gitlab.flux.utah.edu/openzms/openapi-python-client.git@openzms#egg=427f6c93",
]
dev = [
    "setuptools>=61,<81.0.0",
    "setuptools_scm>=7",
    "build",
    "wheel",
    "sphinx",
    "sphinx-autodoc-typehints",
    "sphinx-autoapi",
    "sphinxcontrib-redoc @ git+https://gitlab.flux.utah.edu/stoller/sphinx-redoc.git",
    # yq requires jq which is an apt install
    "yq",
]

[project.scripts]
portal-cli = "cloudlabclient.cli.__main__:main"
portal-tokens = "cloudlabclient.common.gettokens:main"

[project.urls]
Homepage = "https://cloudlab.us"
Source = "https://gitlab.flux.utah.edu/emulab/portal-api.git"

[tool.setuptools.dynamic]
version = {attr = "cloudlabclient.__version__"}
readme = {file = ["README.md"]}

#[tool.setuptools]
#packages = [
#    "client",
#    "client.cli",
#    "client.portal.v1"
#]

[tool.setuptools.packages.find]
where = ["."]
include = [
    "cloudlabclient*",
]
exclude = [
    "test*",
]
namespaces = false

[tool.setuptools_scm]
```
