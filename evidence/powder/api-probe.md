# POWDER Portal API probe

- Checked UTC: 2026-08-24T17:00:26Z
- WellPulse SHA: bc3187aa75c0ca7b38ee57c45eb75f5b63fcb87e
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
```

## Python/package metadata
```text
--- pyproject.toml ---
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

## Candidate CLI entry points and examples
```text
/tmp/portal-api/openapi.json:43:                "description": "The target experiment ID.",
/tmp/portal-api/openapi.json:188:                    "experiment"
/tmp/portal-api/openapi.json:223:                "description": "A cloudlab experiment.",
/tmp/portal-api/openapi.json:226:                        "description": "Unique identifier of the experiment.",
/tmp/portal-api/openapi.json:233:                        "description": "A human readable name for the experiment .",
/tmp/portal-api/openapi.json:238:                        "description": "The project the experiment is instantiated in.",
/tmp/portal-api/openapi.json:243:                        "description": "The project subgroup the experiment is instantiated in.",
/tmp/portal-api/openapi.json:248:                        "description": "ID of the profile used to create the experiment",
/tmp/portal-api/openapi.json:280:                        "description": "The creation time of the experiment",
/tmp/portal-api/openapi.json:287:                        "description": "The time the experiment is scheduled to start at",
/tmp/portal-api/openapi.json:294:                        "description": "The time the experiment is scheduled to stop at",
/tmp/portal-api/openapi.json:301:                        "description": "The time the experiment was actually started",
/tmp/portal-api/openapi.json:309:                        "description": "The current expiration time of the experiment (will be auto reaped)",
/tmp/portal-api/openapi.json:315:                        "description": "Current status of the experiment.",
/tmp/portal-api/openapi.json:321:                        "description": "The ID of the experiments WB store.",
/tmp/portal-api/openapi.json:341:                        "description": "The refspec of the experiment (for repo backed profiles)",
/tmp/portal-api/openapi.json:347:                        "description": "The commit hash of the experiment (for repo backed profiles)",
/tmp/portal-api/openapi.json:359:                        "description": "List of aggregates in the experiment",
/tmp/portal-api/openapi.json:375:                        "description": "Additional ssh public key for the experiment",
/tmp/portal-api/openapi.json:387:                "description": "Create a cloudlab experiment.",
/tmp/portal-api/openapi.json:390:                        "description": "A human readable name for the experiment",
/tmp/portal-api/openapi.json:395:                        "description": "The project the experiment is instantiated in.",
/tmp/portal-api/openapi.json:400:                        "description": "The project subgroup the experiment is instantiated in.",
/tmp/portal-api/openapi.json:418:                        "description": "Schedule experiment to start at a future time",
/tmp/portal-api/openapi.json:425:                        "description": "Schedule experiment to stop at a future time",
/tmp/portal-api/openapi.json:431:                        "description": "Initial experiment duration in hours",
/tmp/portal-api/openapi.json:458:                        "description": "Additional ssh public key for the experiment.",
/tmp/portal-api/openapi.json:473:                "description": "Modify a running experiment",
/tmp/portal-api/openapi.json:517:                        "description": "Current status of the experiment.",
/tmp/portal-api/openapi.json:536:                    "experiments": {
/tmp/portal-api/openapi.json:546:                "description": "Extend a running experiment, with a duration, additional number of hours, or an explicit end time",
/tmp/portal-api/openapi.json:549:                        "description": "Set the experiment expiration to GMT Date/Time",
/tmp/portal-api/openapi.json:556:                        "description": "Number of hours to add to the current experiment expiration",
/tmp/portal-api/openapi.json:623:                "description": "Perform operational action on a node in an experiment",
/tmp/portal-api/openapi.json:1216:                        "description": "The profile can be instantiated by any user",
/tmp/portal-api/openapi.json:1319:                        "description": "The profile can be instantiated by any user",
/tmp/portal-api/openapi.json:1355:                        "description": "The profile can be instantiated by any user",
/tmp/portal-api/openapi.json:1397:                "name": "experiment_id",
/tmp/portal-api/openapi.json:1403:                            "summary": "UUID of an experiment"
/tmp/portal-api/openapi.json:1406:                            "value": "myproject,myexperiment",
/tmp/portal-api/openapi.json:1407:                            "summary": "Project,Name of an experiment"
/tmp/portal-api/openapi.json:1411:                "description": "The target experiment.",
/tmp/portal-api/openapi.json:1416:                        "summary": "UUID of an experiment"
/tmp/portal-api/openapi.json:1419:                        "value": "myproject,myexperiment",
/tmp/portal-api/openapi.json:1420:                        "summary": "Project,Name of an experiment"
/tmp/portal-api/openapi.json:1468:                        "value": "myproject,myexperiment",
/tmp/portal-api/openapi.json:1599:                        "description": "List of experiments."
/tmp/portal-api/openapi.json:1632:                            "$ref": "../examples/tokenRefresh.sh"
/tmp/portal-api/openapi.json:1638:                            "$ref": "../examples/tokenRefresh.py"
/tmp/portal-api/openapi.json:1651:                        "description": "List of experiments."
/tmp/portal-api/openapi.json:1710:        "/experiments": {
/tmp/portal-api/openapi.json:1712:                "description": "Get experiment list",
/tmp/portal-api/openapi.json:1726:                        "name": "experiment_id",
/tmp/portal-api/openapi.json:1731:                        "description": "Filter by experiment id.",
/tmp/portal-api/openapi.json:1757:                            "$ref": "../examples/experimentStatus.sh"
/tmp/portal-api/openapi.json:1763:                            "$ref": "../examples/experimentStatus.py"
/tmp/portal-api/openapi.json:1776:                        "description": "List of experiments."
/tmp/portal-api/openapi.json:1790:                "description": "Create a new experiment.",
/tmp/portal-api/openapi.json:1813:                            "$ref": "../examples/experimentCreate.sh"
/tmp/portal-api/openapi.json:1819:                            "$ref": "../examples/experimentCreate.py"
/tmp/portal-api/openapi.json:1875:                        "description": "Load average too high or too many experiments waiting",
/tmp/portal-api/openapi.json:1897:        "/experiments/{experiment_id}": {
/tmp/portal-api/openapi.json:1899:                "description": "Retrieve a specific experiment.",
/tmp/portal-api/openapi.json:1924:                        "description": "An experiment object."
/tmp/portal-api/openapi.json:1969:                "description": "Extend a running experiment, with a duration, number of additional hours, or an explicit end time",
/tmp/portal-api/openapi.json:1995:                            "$ref": "../examples/experimentExtend.sh"
/tmp/portal-api/openapi.json:2001:                            "$ref": "../examples/experimentExtend.py"
/tmp/portal-api/openapi.json:2059:                "description": "Modify a running experiment",
/tmp/portal-api/openapi.json:2085:                            "$ref": "../examples/experimentModify.sh"
/tmp/portal-api/openapi.json:2091:                            "$ref": "../examples/experimentModify.py"
/tmp/portal-api/openapi.json:2149:                "description": "Terminate an experiment.",
/tmp/portal-api/openapi.json:2150:                "operationId": "terminateExperiment",
/tmp/portal-api/openapi.json:2166:                            "$ref": "../examples/experimentTerminate.sh"
/tmp/portal-api/openapi.json:2172:                            "$ref": "../examples/experimentTerminate.py"
/tmp/portal-api/openapi.json:2223:        "/experiments/{experiment_id}/manifests": {
/tmp/portal-api/openapi.json:2225:                "description": "Retrieve manifests for a running experiment.",
/tmp/portal-api/openapi.json:2247:                        "description": "An array of manifests"
/tmp/portal-api/openapi.json:2292:        "/experiments/{experiment_id}/vlan/{source_lan}/connect": {
/tmp/portal-api/openapi.json:2294:                "description": "Connect a shared vlan in an experiment to another experiment's shared vlan.",
/tmp/portal-api/openapi.json:2321:                        "description": "The experiment to connect to",
/tmp/portal-api/openapi.json:2327:                        "description": "The client ID of the lan in the target experiment",
/tmp/portal-api/openapi.json:2381:        "/experiments/{experiment_id}/vlan/{source_lan}/disconnect": {
/tmp/portal-api/openapi.json:2383:                "description": "Disonnect a shared vlan in an experiment from another experiment's shared vlan.",
/tmp/portal-api/openapi.json:2452:        "/experiments/{experiment_id}/node/{client_id}": {
/tmp/portal-api/openapi.json:2454:                "description": "Get info about a specific node in an experiment",
/tmp/portal-api/openapi.json:2534:        "/experiments/{experiment_id}/nodes/reboot": {
/tmp/portal-api/openapi.json:2536:                "description": "Reboot all nodes in an experiment",
/tmp/portal-api/openapi.json:2553:                            "$ref": "../examples/experimentOp.sh"
/tmp/portal-api/openapi.json:2559:                            "$ref": "../examples/experimentOp.py"
/tmp/portal-api/openapi.json:2627:        "/experiments/{experiment_id}/nodes/reload": {
/tmp/portal-api/openapi.json:2629:                "description": "Reload all nodes in an experiment",
/tmp/portal-api/openapi.json:2646:                            "$ref": "../examples/experimentOp.sh"
/tmp/portal-api/openapi.json:2652:                            "$ref": "../examples/experimentOp.py"
/tmp/portal-api/openapi.json:2720:        "/experiments/{experiment_id}/nodes/start": {
/tmp/portal-api/openapi.json:2722:                "description": "Start all nodes in an experiment",
/tmp/portal-api/openapi.json:2739:                            "$ref": "../examples/experimentOp.sh"
/tmp/portal-api/openapi.json:2745:                            "$ref": "../examples/experimentOp.py"
/tmp/portal-api/openapi.json:2813:        "/experiments/{experiment_id}/nodes/stop": {
/tmp/portal-api/openapi.json:2815:                "description": "Stop all nodes in an experiment",
/tmp/portal-api/openapi.json:2832:                            "$ref": "../examples/experimentOp.sh"
/tmp/portal-api/openapi.json:2838:                            "$ref": "../examples/experimentOp.py"
/tmp/portal-api/openapi.json:2906:        "/experiments/{experiment_id}/nodes/powercycle": {
/tmp/portal-api/openapi.json:2908:                "description": "Power cycle all nodes in an experiment",
/tmp/portal-api/openapi.json:2925:                            "$ref": "../examples/experimentOp.sh"
/tmp/portal-api/openapi.json:2931:                            "$ref": "../examples/experimentOp.py"
/tmp/portal-api/openapi.json:2999:        "/experiments/{experiment_id}/snapshot/{client_id}": {
/tmp/portal-api/openapi.json:3001:                "description": "Snapshot (take an image of) a node in an experiment",
/tmp/portal-api/openapi.json:3030:                            "$ref": "../examples/experimentSnapshot.sh"
/tmp/portal-api/openapi.json:3036:                            "$ref": "../examples/experimentSnapshot.py"
/tmp/portal-api/openapi.json:3104:        "/experiments/{experiment_id}/snapshot/{snapshot_id}": {
/tmp/portal-api/openapi.json:3194:        "/experiments/{experiment_id}/node/{client_id}/reboot": {
/tmp/portal-api/openapi.json:3196:                "description": "Reboot a node in an experiment",
/tmp/portal-api/openapi.json:3216:                            "$ref": "../examples/experimentNodeOp.sh"
/tmp/portal-api/openapi.json:3222:                            "$ref": "../examples/experimentNodeOp.py"
/tmp/portal-api/openapi.json:3290:        "/experiments/{experiment_id}/node/{client_id}/reload": {
/tmp/portal-api/openapi.json:3292:                "description": "Reload a node in an experiment",
/tmp/portal-api/openapi.json:3312:                            "$ref": "../examples/experimentNodeOp.sh"
/tmp/portal-api/openapi.json:3318:                            "$ref": "../examples/experimentNodeOp.py"
/tmp/portal-api/openapi.json:3386:        "/experiments/{experiment_id}/node/{client_id}/stop": {
/tmp/portal-api/openapi.json:3388:                "description": "Stop a node in an experiment",
/tmp/portal-api/openapi.json:3408:                            "$ref": "../examples/experimentNodeOp.sh"
/tmp/portal-api/openapi.json:3414:                            "$ref": "../examples/experimentNodeOp.py"
/tmp/portal-api/openapi.json:3482:        "/experiments/{experiment_id}/node/{client_id}/start": {
/tmp/portal-api/openapi.json:3484:                "description": "Start a stopped node in an experiment",
/tmp/portal-api/openapi.json:3504:                            "$ref": "../examples/experimentNodeOp.sh"
/tmp/portal-api/openapi.json:3510:                            "$ref": "../examples/experimentNodeOp.py"
/tmp/portal-api/openapi.json:3578:        "/experiments/{experiment_id}/node/{client_id}/powercycle": {
/tmp/portal-api/openapi.json:3580:                "description": "Power cycle a node in an experiment",
/tmp/portal-api/openapi.json:3600:                            "$ref": "../examples/experimentNodeOp.sh"
/tmp/portal-api/openapi.json:3606:                            "$ref": "../examples/experimentNodeOp.py"
/tmp/portal-api/openapi.json:3726:                        "description": "List of experiments."
/tmp/portal-api/openapi.json:4602:                        "description": "Load average too high or too many experiments waiting",
/tmp/portal-api/README.md:71:For example, to get a list of your experiments:
/tmp/portal-api/README.md:73:	mypc> portal-api experiment list
/tmp/portal-api/README.md:119:	explist = Portal.list_experiments()
/tmp/portal-api/README.md:120:	print(str(explist.experiments))
/tmp/portal-api/README.md:133:### Creating an experiment
/tmp/portal-api/README.md:140:are the bindings we are going to use to instantiate a 1 node
/tmp/portal-api/README.md:141:experiment at the Emulab cluster:
/tmp/portal-api/README.md:150:start this experiment, and have it terminate in one hour:
/tmp/portal-api/README.md:152:	EXPID=`portal-cli experiment create --name apitest --project myproject \
/tmp/portal-api/README.md:154:		--bindings @cloudlabclient/tests/experiments/bindings-1node.json | jq -r .id`
/tmp/portal-api/README.md:167:	myexp = Portal.create_experiment(body = ExperimentCreate(
/tmp/portal-api/README.md:180:### Getting experiment status
/tmp/portal-api/README.md:182:To get the experiment status you need the experiment ID (from
/tmp/portal-api/README.md:184:`create_experiment` and has been slightly abbreviated:
/tmp/portal-api/README.md:186:	portal-cli experiment get --experiment-id $EXPID
/tmp/portal-api/README.md:221:### Modify an experiment.
/tmp/portal-api/README.md:223:Experiments that are instantiated from `parameterized profiles` can be
/tmp/portal-api/README.md:226:that were supplied when creating the experiment. Using the one node
/tmp/portal-api/README.md:236:command line to start the experiment modification is:
/tmp/portal-api/README.md:238:	portal-cli experiment modify --experiment-id $EXPID \
/tmp/portal-api/README.md:239:		--bindings @cloudlabclient/tests/experiments/bindings-2node.json
/tmp/portal-api/README.md:241:### Getting experiment manifests
/tmp/portal-api/README.md:243:Once the experiment is ready, you can ask for the manifests(s):
/tmp/portal-api/README.md:245:	portal-cli experiment manifests get --experiment-id $EXPID
/tmp/portal-api/README.md:250:### Terminating an experiment
/tmp/portal-api/README.md:252:	portal-cli experiment terminate --experiment-id $EXPID
/tmp/portal-api/README.md:256:	portal-cli experiment get --experiment-id $EXPID
/tmp/portal-api/README.md:259:		"error": "No such experiment",
/tmp/portal-api/README.md:262:### Extending an experiment
/tmp/portal-api/README.md:269:approved (or rejected). The return value is the new experiment status,
/tmp/portal-api/README.md:273:	portal-cli experiment extend --experiment-id $EXPID --extend-by 2
/tmp/portal-api/README.md:277:	portal-cli experiment extend --experiment-id $EXPID --expires-at "2025-07-28T19:01:30+00:00"
/tmp/portal-api/README.md:284:	portal-cli experiment extend --experiment-id $EXPID --extend-by 2
/tmp/portal-api/README.md:287:### Reboot/reload/powercycle/stop/start nodes in an experiment
/tmp/portal-api/README.md:289:Reboot (or reload, powercycle, stop, start) nodes in an experiment.
/tmp/portal-api/README.md:292:	portal-cli experiment node reboot --experiment-id $EXPID --client-id node0
/tmp/portal-api/README.md:294:or for all nodes in an experiment:
/tmp/portal-api/README.md:296:	portal-cli experiment nodes reboot --experiment-id $EXPID
/tmp/portal-api/README.md:300:### Taking an image snapshot of a node in an experiment
/tmp/portal-api/README.md:306:Both the experiment and the node must be in the `ready` state to start
/tmp/portal-api/README.md:309:instantiated profile source code.
/tmp/portal-api/README.md:313:    SNAPID=`portal-cli experiment snapshot start --experiment-id $EXPID \
/tmp/portal-api/README.md:319:	portal-cli experiment snapshot get --experiment-id $EXPID --snapshot-id $SNAPID`
/tmp/portal-api/cloudlabclient/examples/experimentExtend.sh:3:# Extend the experiment created earlier. Here we use the extend_by
/tmp/portal-api/cloudlabclient/examples/experimentExtend.sh:8:   experiment extend --experiment-id $EXPID --extend-by 1
/tmp/portal-api/cloudlabclient/examples/experimentOp.sh:3:# Perform an operation on all nodes in an experiment.
/tmp/portal-api/cloudlabclient/examples/experimentOp.sh:7:   experiment nodes [reboot|reload|powercycle|stop|start] --experiment-id $EXPID
/tmp/portal-api/cloudlabclient/examples/experimentList.py:10:explist = Portal.list_experiments()
/tmp/portal-api/cloudlabclient/examples/experimentTerminate.sh:3:# Terminate an experiment
/tmp/portal-api/cloudlabclient/examples/experimentTerminate.sh:7:   experiment terminate --experiment-id $EXPID
/tmp/portal-api/cloudlabclient/examples/experimentStatus.py:3:# Get the status of an experiment
/tmp/portal-api/cloudlabclient/examples/experimentStatus.py:12:myexp = Portal.get_experiment(EXPID)
/tmp/portal-api/cloudlabclient/examples/experimentModify.sh:3:# Modify the one node experiment we created earlier into a
/tmp/portal-api/cloudlabclient/examples/experimentModify.sh:4:# two node experiment.
/tmp/portal-api/cloudlabclient/examples/experimentModify.sh:8:   experiment modify --experiment-id $EXPID \
/tmp/portal-api/cloudlabclient/examples/experimentModify.sh:9:	--bindings @cloudlabclient/tests/experiments/bindings-2node.json
/tmp/portal-api/cloudlabclient/examples/experimentNodeOp.py:3:# Perform an operation on a specific node in an experiment.  Use the
/tmp/portal-api/cloudlabclient/examples/experimentNodeOp.py:12:Portal.[reboot|reload|powercycle|start|stop]_experiment_node(EXPID, "node0")
/tmp/portal-api/cloudlabclient/examples/experimentCreate.py:3:# Create a one node experiment that expires in one hour.
/tmp/portal-api/cloudlabclient/examples/experimentCreate.py:8:# instantiate a 1 node experiment at the Emulab cluster:
/tmp/portal-api/cloudlabclient/examples/experimentCreate.py:17:myexp = Portal.create_experiment(body = ExperimentCreate(
/tmp/portal-api/cloudlabclient/examples/experimentExtend.py:3:# Extend the experiment created earlier. Here we use the extend_by
/tmp/portal-api/cloudlabclient/examples/experimentExtend.py:13:myexp = Portal.extend_experiment(
/tmp/portal-api/cloudlabclient/examples/experimentModify.py:3:# Modify the one node experiment we created earlier into a
/tmp/portal-api/cloudlabclient/examples/experimentModify.py:4:# two node experiment.
/tmp/portal-api/cloudlabclient/examples/experimentModify.py:13:myexp = Portal.modify_experiment(EXPID, body = ExperimentModify(
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.py:3:# Initiate an image snapshot on a specific node in an experiment.  Use
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.py:9:# snapshot has failed.  Both the experiment and the node must be in
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.py:19:status = Portal.start_experiment_snapshot(
/tmp/portal-api/cloudlabclient/examples/experimentNodeOp.sh:3:# Perform an operation on a specific node in an experiment.  Use the
/tmp/portal-api/cloudlabclient/examples/experimentNodeOp.sh:8:   experiment node [reboot|reload|powercycle|stop|start] \
/tmp/portal-api/cloudlabclient/examples/experimentNodeOp.sh:9:     --experiment-id $EXPID --client-id node0
/tmp/portal-api/cloudlabclient/examples/experimentOp.py:3:# Perform an operation on all nodes in an experiment.
/tmp/portal-api/cloudlabclient/examples/experimentOp.py:11:Portal.[reboot|reload|powercycle|start|stop]_experiment_nodes(EXPID)
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.sh:3:# Initiate an image snapshot on a specific node in an experiment.  Use
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.sh:9:# snapshot has failed.  Both the experiment and the node must be in
/tmp/portal-api/cloudlabclient/examples/experimentSnapshot.sh:14:   experiment snapshot --experiment-id $EXPID \
/tmp/portal-api/cloudlabclient/examples/experimentStatus.sh:3:# Get experiment status. $EXPID is the ID of the experiment
/tmp/portal-api/cloudlabclient/examples/experimentStatus.sh:4:# that was returned when the experiment was created.
/tmp/portal-api/cloudlabclient/examples/experimentStatus.sh:8:	   experiment get --experiment-id $EXPID
/tmp/portal-api/cloudlabclient/examples/experimentCreate.sh:3:# Create a one node experiment that expires in one hour.
/tmp/portal-api/cloudlabclient/examples/experimentCreate.sh:10:# are the bindings we are going to use to instantiate a 1 node
/tmp/portal-api/cloudlabclient/examples/experimentCreate.sh:11:# experiment at the Emulab cluster:
/tmp/portal-api/cloudlabclient/examples/experimentCreate.sh:15:   experiment create --name apitest --project testbed \
/tmp/portal-api/cloudlabclient/examples/experimentCreate.sh:17:     --bindings @cloudlabclient/tests/experiments/bindings-1node.json
/tmp/portal-api/cloudlabclient/examples/experimentTerminate.py:3:# Terminate the experiment created earlier
/tmp/portal-api/cloudlabclient/examples/experimentTerminate.py:11:Portal.terminate_experiment(EXPID);
/tmp/portal-api/cloudlabclient/common/manifest.py:14:manifest = None
/tmp/portal-api/cloudlabclient/common/manifest.py:46:def parse_manifest():
/tmp/portal-api/cloudlabclient/common/manifest.py:47:    global manifest
/tmp/portal-api/cloudlabclient/common/manifest.py:49:    if not manifest:
/tmp/portal-api/cloudlabclient/common/manifest.py:50:        proc = subprocess.run([TMCC,"geni_manifest"], capture_output=True)
/tmp/portal-api/cloudlabclient/common/manifest.py:53:        manifest = proc.stdout.decode().lstrip("\0")
/tmp/portal-api/cloudlabclient/common/manifest.py:55:    root = lxml.etree.fromstring(manifest)
/tmp/portal-api/cloudlabclient/common/manifest.py:57:    manifest_dict = dict()
/tmp/portal-api/cloudlabclient/common/manifest.py:70:    manifest_dict["nodes"] = nodes
/tmp/portal-api/cloudlabclient/common/manifest.py:71:    manifest_dict["nodenames"] = list(nodes)
/tmp/portal-api/cloudlabclient/common/manifest.py:85:    manifest_dict["parameters"] = parameters
/tmp/portal-api/cloudlabclient/common/manifest.py:99:    manifest_dict["routable_pools"] = routable_pools
/tmp/portal-api/cloudlabclient/common/manifest.py:107:    manifest_dict["passwords"] = passwords
/tmp/portal-api/cloudlabclient/common/manifest.py:116:    manifest_dict["rdzinfo"] = rdzinfo
/tmp/portal-api/cloudlabclient/common/manifest.py:128:    manifest_dict["spectrum"] = spectrum
/tmp/portal-api/cloudlabclient/common/manifest.py:130:    return manifest_dict
/tmp/portal-api/cloudlabclient/common/manifest.py:134:    manifest_dict = parse_manifest();
/tmp/portal-api/cloudlabclient/common/manifest.py:136:    if not manifest_dict:
/tmp/portal-api/cloudlabclient/common/manifest.py:139:    passwords = manifest_dict["passwords"]
/tmp/portal-api/cloudlabclient/common/manifest.py:140:    if "experiment-rpctoken" in passwords:
/tmp/portal-api/cloudlabclient/common/manifest.py:141:        tokens["experiment"] = passwords["experiment-rpctoken"]
/tmp/portal-api/cloudlabclient/common/manifest.py:150:    print(str(parse_manifest()))
/tmp/portal-api/cloudlabclient/common/gettokens.py:1:import argparse
/tmp/portal-api/cloudlabclient/common/gettokens.py:7:from cloudlabclient.common.manifest import getAPITokens
/tmp/portal-api/cloudlabclient/common/gettokens.py:10:    argparser = argparse.ArgumentParser(description="Get API tokens from Portal manifest")
/tmp/portal-api/cloudlabclient/common/gettokens.py:11:    argparser.add_argument(
/tmp/portal-api/cloudlabclient/common/gettokens.py:13:    args = argparser.parse_args(sys.argv[1:])
/tmp/portal-api/cloudlabclient/tests/__init__.py:1:import argparse
/tmp/portal-api/cloudlabclient/tests/__init__.py:4:class DefaultDestEnvAction(argparse.Action):
/tmp/portal-api/cloudlabclient/tests/__init__.py:6:        """An argparse.Action that initializes the default value of the arg from an environment variable named `dest.upper()` (where dest is the storage location of the value post-parse, e.g. `args.dest`); and, if the arg was required, *unsets* it from being required, so that argparse does not fail the parse if the argument is not supplied.  This is certainly a bit unfortunate since it changes the helptext behavior, but nothing to do about that."""
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:4:# Test experiment APIs
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:9:echo "Creating experiment, patience please"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:10:EXPT=`$PORTALAPI experiment create --name apitest --project testbed \
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:12:	--bindings @client/tests/experiments/bindings-1node.json`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:15:    echo "Could not create experiment"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:20:    echo "Could not get experiment ID"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:31:    EXPTSTATUS=`$PORTALAPI experiment get --experiment-id $ID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:34:	echo "Could not get experiment status"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:46:    echo "Extending the experiment for 2 hours"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:47:    EXTEND=`$PORTALAPI experiment extend --experiment-id $ID --duration 2`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:50:	echo "Could not extend experiment"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:56:    echo "Modifying experiment"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:57:    MODIFY=`$PORTALAPI experiment modify --experiment-id $ID \
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:58:	       --bindings @client/tests/experiments/bindings-2node.json`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:61:	echo "Could not modify experiment"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:70:	    EXPTSTATUS=`$PORTALAPI experiment get --experiment-id $ID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:73:		echo "Could not get experiment status"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:90:    SNAPSHOT=`$PORTALAPI experiment snapshot start --experiment-id $ID \
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:104:	    SNAPSTATUS=`$PORTALAPI experiment snapshot get \
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:105:    		     --experiment-id $ID --snapshot-id $SNAPID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:119:	# Lets wait for the experiment to get back to ready before proceeding.
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:120:	echo "Waiting for experiment to go back to ready"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:127:	    EXPTSTATUS=`$PORTALAPI experiment get --experiment-id $ID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:130:		echo "Could not get experiment status"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:146:    REBOOT=`$PORTALAPI experiment node reboot --experiment-id $ID --client-id $CLIENTID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:154:	NODE=`$PORTALAPI experiment node get --experiment-id $ID --client-id $CLIENTID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:167:echo "Terminating experiment"
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:168:TERMINATE=`$PORTALAPI experiment delete --experiment-id $ID`
/tmp/portal-api/cloudlabclient/tests/experiments/experimentTest.sh:171:    echo "Could not terminate experiment"
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:11:from .experiment import Experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:12:from .experiment_aggregates import ExperimentAggregates
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:13:from .experiment_create import ExperimentCreate
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:14:from .experiment_list import ExperimentList
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:15:from .experiment_modify import ExperimentModify
/tmp/portal-api/cloudlabclient/portal/v1/models/__init__.py:17:from .manifest_array import ManifestArray
/tmp/portal-api/cloudlabclient/portal/v1/models/aggregate_status.py:21:        status (Union[Unset, str]): Current status of the experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:12:    from ..models.experiment_aggregates import ExperimentAggregates
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:20:    """A cloudlab experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:23:        id (str): Unique identifier of the experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:24:        name (Union[Unset, str]): A human readable name for the experiment .
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:25:        project (Union[Unset, str]): The project the experiment is instantiated in.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:26:        group (Union[Unset, str]): The project subgroup the experiment is instantiated in.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:27:        profile_id (Union[Unset, str]): ID of the profile used to create the experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:32:        created_at (Union[Unset, datetime.datetime]): The creation time of the experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:33:        start_at (Union[None, Unset, datetime.datetime]): The time the experiment is scheduled to start at
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:34:        stop_at (Union[None, Unset, datetime.datetime]): The time the experiment is scheduled to stop at
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:35:        started_at (Union[None, Unset, datetime.datetime]): The time the experiment was actually started
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:36:        expires_at (Union[None, Unset, datetime.datetime]): The current expiration time of the experiment (will be auto
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:38:        status (Union[Unset, str]): Current status of the experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:39:        wbstore_id (Union[Unset, str]): The ID of the experiments WB store.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:42:        repository_refspec (Union[None, Unset, str]): The refspec of the experiment (for repo backed profiles)
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:43:        repository_hash (Union[None, Unset, str]): The commit hash of the experiment (for repo backed profiles)
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:45:        aggregates (Union[Unset, ExperimentAggregates]): List of aggregates in the experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:47:        sshpubkey (Union[None, Unset, str]): Additional ssh public key for the experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:260:        from ..models.experiment_aggregates import ExperimentAggregates
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:423:        experiment = cls(
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:450:        experiment.additional_properties = d
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:451:        return experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment.py:472:    from ..models.experiment_aggregates import ExperimentAggregates
/tmp/portal-api/cloudlabclient/portal/v1/models/manifest_array.py:25:        manifest_array = cls()
/tmp/portal-api/cloudlabclient/portal/v1/models/manifest_array.py:27:        manifest_array.additional_properties = d
/tmp/portal-api/cloudlabclient/portal/v1/models/manifest_array.py:28:        return manifest_array
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:19:    """Create a cloudlab experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:22:        name (str): A human readable name for the experiment
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:23:        project (str): The project the experiment is instantiated in.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:26:        group (Union[None, Unset, str]): The project subgroup the experiment is instantiated in.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:27:        start_at (Union[None, Unset, datetime.datetime]): Schedule experiment to start at a future time
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:28:        stop_at (Union[None, Unset, datetime.datetime]): Schedule experiment to stop at a future time
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:29:        duration (Union[None, Unset, int]): Initial experiment duration in hours
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:35:        sshpubkey (Union[None, Unset, str]): Additional ssh public key for the experiment.
/tmp/portal-api/cloudlabclient/portal/v1/models/experiment_create.py:265:        experiment_create = cls(
```
