"""implementation of the gRPC server for the fake detection service"""

import logging
import grpc
import fake_detect_pb2
import fake_detect_pb2_grpc

from ..py import fake_detector
from ..py import data_layer

class FakeDetect(fake_detect_pb2_grpc.FakeDetectServiceServicer):
    """implementation of the gRPC server for the fake detection service"""
    def __init__(self) -> None:
        self._detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())
        logging.basicConfig(level=logging.DEBUG, filename='grpc.log', format='%(asctime)s - %(levelname)s - %(message)s')
    
    def CheckUsername(self, request, context):
        """check single username"""
        logging.info("CheckUsername: {}".format(request.username))
        response = fake_detect_pb2.CheckUsernameResponse()
        response.is_fake = self._detector.is_fake(request.username)
        return response
    
    def CheckUsernames(self, request, context):
        """check multiple usernames"""
        logging.info("CheckUsernames: {}".format(request.usernames))
        # TODO: implement request size limits
        response = fake_detect_pb2.CheckUsernamesResponse()
        response.is_fake.extend([username for username in request.usernames if self._detector.is_fake(username)])
        return response