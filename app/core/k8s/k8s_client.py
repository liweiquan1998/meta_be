from kubernetes.client import api_client
from kubernetes.client.apis import core_v1_api
from kubernetes import client


class KubernetesTools(object):
    def __init__(self):
        self.k8s_url = "https://192.168.199.109:6443"  # todo 改成配置项

    def get_token(self):
        """
        获取token
        :return:
        """
        return "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhTMXExTDJkUXBtMWZnWHE3SGgwVGtlMjdYZlAtQTlHYWdXSWlybmY4VEkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTc1bWo1Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJiZWI1MjhkNC1jMmUxLTRiMjgtYTYyNC1iYWI5NjgzNjg2NTAiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.a9TBKjgcEVSI6pDvqqfhq8NBJFcSCD4xEGI9Ne_KXfURXODUAmiM8Ld480BZudFo-RKnaWxZXUUUgQCcqH7pjsV-YrB27Lh4aySjaNfxXt-euecCF17XheP_g7K1p3XP1eS07FP-8KgHeo_p9TZK8PotR9zux5SsExuOAd7VUCLvUeWllPkLrsN6woTbDWnJTNCqfwtP04BOiDCiQpOwqfd8S1bby1lwWWI6pxM0cK1_lPQc6YydB-nB4mQRNe4qCwVx_qG_NTzSiI9uel1m0OVIZg2ungsjTzSInSTyaWjJ8V0T8uovDNTZv0_aC4DHEW7X14xtLY9UiZNy50Nebg"

    def get_api(self):
        """
        获取API的CoreV1Api版本对象
        :return:
        """
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + self.get_token()}
        client1 = api_client.ApiClient(configuration=configuration)
        api = core_v1_api.CoreV1Api(client1)
        return api

    def get_namespace_list(self):
        """
        获取命名空间列表
        :return:
        """
        api = self.get_api()
        namespace_list = []

        for ns in api.list_namespace().items:
            namespace_list.append(ns.metadata.name)

        return namespace_list

    def get_pod_logs(self, namespaces, labels: dict, tail_lines=10000):
        """
        查看pod日志
        :param namespaces: 命令空间，比如：default
        :param pod_name: pod完整名称，比如：flaskapp-1-5d96dbf59b-lhmp8
        :return:
        """
        api = self.get_api()
        rets = api.list_namespaced_pod(namespaces, label_selector=','.join([f'{k}={v}' for k, v in labels.items()]),
                                       watch=False)
        if len(rets.items) > 0:
            pod_name = rets.items[0].to_dict()['metadata']['name']
            log_content = api.read_namespaced_pod_log(pod_name, namespaces, pretty=True, tail_lines=tail_lines)
            return log_content
        else:
            return None
