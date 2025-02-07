import requests

BASE_URL = "http://localhost:8080"


def test_get_fibonacci():
    response = requests.get(f"{BASE_URL}/100")
    assert response.status_code == 200
    assert response.json() == {"sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]}


def test_get_fibonaaci_paged():
    response_0 = requests.get(f"{BASE_URL}/1000000000000000000000/paged?page_number=0")
    assert response_0.status_code == 200
    assert response_0.json() == {
        "page_number": 0,
        "total_pages": 2,
        "sequence": [
            0,
            1,
            1,
            2,
            3,
            5,
            8,
            13,
            21,
            34,
            55,
            89,
            144,
            233,
            377,
            610,
            987,
            1597,
            2584,
            4181,
            6765,
            10946,
            17711,
            28657,
            46368,
            75025,
            121393,
            196418,
            317811,
            514229,
            832040,
            1346269,
            2178309,
            3524578,
            5702887,
            9227465,
            14930352,
            24157817,
            39088169,
            63245986,
            102334155,
            165580141,
            267914296,
            433494437,
            701408733,
            1134903170,
            1836311903,
            2971215073,
            4807526976,
            7778742049,
            12586269025,
            20365011074,
            32951280099,
            53316291173,
            86267571272,
            139583862445,
            225851433717,
            365435296162,
            591286729879,
            956722026041,
            1548008755920,
            2504730781961,
            4052739537881,
            6557470319842,
            10610209857723,
            17167680177565,
            27777890035288,
            44945570212853,
            72723460248141,
            117669030460994,
            190392490709135,
            308061521170129,
            498454011879264,
            806515533049393,
            1304969544928657,
            2111485077978050,
            3416454622906707,
            5527939700884757,
            8944394323791464,
            14472334024676221,
            23416728348467685,
            37889062373143906,
            61305790721611591,
            99194853094755497,
            160500643816367088,
            259695496911122585,
            420196140727489673,
            679891637638612258,
            1100087778366101931,
            1779979416004714189,
            2880067194370816120,
            4660046610375530309,
            7540113804746346429,
            12200160415121876738,
            19740274219868223167,
            31940434634990099905,
            51680708854858323072,
            83621143489848422977,
            135301852344706746049,
            218922995834555169026,
        ],
    }

    response_1 = requests.get(f"{BASE_URL}/1000000000000000000000/paged?page_number=1")
    assert response_1.status_code == 200
    assert response_1.json() == {
        "page_number": 1,
        "total_pages": 2,
        "sequence": [
            354224848179261915075,
            573147844013817084101,
            927372692193078999176,
        ],
    }


def test_get_fibonaaci_paged_invalid_page_number():
    response = requests.get(f"{BASE_URL}/1000000000000000000000/paged?page_number=2")
    assert response.status_code == 400
    assert response.json() == {"detail": "Page number out of bounds"}


def test_add_blacklist():
    payload = {"black_list": 21}
    response = requests.post(f"{BASE_URL}/blacklist", json=payload)
    assert response.status_code == 201
    assert response.json() == {"blacklists": [21]}


def test_add_blacklist_that_already_exists():
    # 21 already added in the previous test
    payload = {"black_list": 21}
    response = requests.post(f"{BASE_URL}/blacklist", json=payload)
    assert response.status_code == 400


def test_add_invalid_blacklist():
    payload = {"black_list": -21}
    response = requests.post(f"{BASE_URL}/blacklist", json=payload)
    assert response.status_code == 400


def test_delete_blacklist():
    # 21 already added in the previous test
    response = requests.delete(f"{BASE_URL}/blacklist/21")
    assert response.status_code == 200
    assert response.json() == {"blacklists": []}

def test_delete_nonexisting_blacklist():
    response = requests.delete(f"{BASE_URL}/blacklist/8")
    assert response.status_code == 404
