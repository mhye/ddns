from library.domain import Dnsapi

def get_para(login_token,domain_name,sub_domain):
    params = dict(login_token=login_token)
    api_1 = Dnsapi(**params)
    resualt = api_1.request("Domain.List")
    domain_id = None
    for domain in resualt.get('domains'):
        if domain.get("name") == domain_name:
            domain_id=domain.get("id")
            break
    if domain_id is None:
        raise Exception("域名不存在")
    params['domain_id'] = domain_id

    api_2 = Dnsapi(**params)
    resault = api_2.request("Record.List")
    record_list = resault.get("records")

    for record in record_list:
        if record.get('name') == sub_domain:
            record_id = record.get('id')
            break

    if record_id is None:
        raise Exception("子域名不存在")
    params.update(dict(
    sub_domain=sub_domain,
    record_id = record_id,
    record_line = "默认"
    ))

    return params
