import syft as sy
import torch as th


def test_message_serde():

    x = sy.Message(0, [1, 2, 3])
    x_bin = sy.serde.serialize(x)
    y = sy.serde.deserialize(x_bin, sy.local_worker)

    assert x.contents == y.contents
    assert x.msg_type == y.msg_type


def test_cmd_message(workers):

    bob = workers["bob"]

    x = th.tensor([1, 2, 3, 4]).send(bob)

    y = x + x  # this is the test

    y = y.get()

    assert (y == th.tensor([2, 4, 6, 8])).all()


def test_obj_message(workers):

    bob = workers["bob"]

    x = th.tensor([1, 2, 3, 4]).send(bob)  # this is the test

    y = x + x

    y = y.get()

    assert (y == th.tensor([2, 4, 6, 8])).all()


def test_obj_req_message(workers):

    bob = workers["bob"]

    x = th.tensor([1, 2, 3, 4]).send(bob)

    y = x + x

    y = y.get()  # this is the test

    assert (y == th.tensor([2, 4, 6, 8])).all()


def test_get_shape_message(workers):

    bob = workers["bob"]

    x = th.tensor([1, 2, 3, 4]).send(bob)

    y = x + x

    z = y.shape  # this is the test

    assert z == th.Size([4])


def test_force_object_delete_message(workers):

    bob = workers["bob"]

    x = th.tensor([1, 2, 3, 4]).send(bob)

    id_on_worker = x.id_at_location

    assert id_on_worker in bob._objects

    del x

    assert id_on_worker not in bob._objects