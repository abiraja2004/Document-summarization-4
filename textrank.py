import sys

import os
import networkx as nx
import math
import time
import operator
import rouge
summary_list=[]
file_list=[]
final_list=[]
final_stripped_list=[]
term_frequency=[]
document_frequency=[]
words=[]
words1=[]
words2=[]
total_unique_words=[]
unique_words=[]
unique_words1=[]
unique_words2=[]
degree_node=[]
final_summary=''
tf1=0
tf2=0
max_degree=0
max_degree_node=0
G=nx.Graph()
topic_name=''
threshold=0
count=0
def graph_construction(topic_name):
	working_path=os.getcwd()
	working_path=working_path+'/'+topic_name
	for file in os.listdir(working_path):
		file_list.append(file)
		
	for file in file_list:
		fp=open(working_path+'/'+file,"r")
		for line in fp:
			strip_line=line.strip('<P></P>\n<DOCNO></DOCNO><DOC></DOC><DATE_TIME></DATE_TIME><BODY></BODY><CATEGORY></CATEGORY><HEADLINE></HEADLINE><TEXT></TEXT>\t ')
		
			final_list.append(strip_line)
	for line in final_list:
		if line!='':
			final_stripped_list.append(line)
		
	
		
	
	for line in final_stripped_list:
		G.add_node(line)
	

def tf_idf(topic_name):
	tf=0
	df=0
	cosine_similarity_list=[]
	cosine_similarity=0
	tf_sentence1=0
	tf_sentence2=0
	df_sentence1=0
	df_sentence2=0
	#calculating term frequency for every word in the sentence
	for i in range(0,len(final_stripped_list)):
		
		words=final_stripped_list[i].split(' ')
		for j in range(0,len(words)):
			total_unique_words.append(words[j])
		unique_words=list(set(words))
		
		for tf_count in range(0,len(unique_words)):
			for count in range(0,len(words)):
				if unique_words[tf_count]==words[count]:
					 tf+=1
			term_frequency.append(tf)
			tf=0
			
			
	#print len(term_frequency)
	for i in range(0,len(total_unique_words)):
	#calculating document frequency for every word in sentence
		for file in file_list:
			working_path=os.getcwd()
			working_path=working_path+'/'+topic_name
			fp=open(working_path+'/'+file,"r")
			for line in fp:
				work=line.strip(' ')
				if total_unique_words[i] in work:
					df+=1
					break			
		document_frequency.append(math.log(len(file_list)/df))
		df=0		
	
	#print len(document_frequency)
	#print len(final_stripped_list)

	for i in range(0,len(final_stripped_list)):
		words1=final_stripped_list[i].split(' ')
		for j in range(i,len(final_stripped_list)):
			words2=final_stripped_list[j].split(' ')
			for k in range(0,len(words1)):
				for l in range(0,len(words2)):
					if words1[k]==words2[l]:
						cosine_similarity=cosine_similarity+document_frequency[i+k]*document_frequency[j+l]
			cosine_similarity_list.append(cosine_similarity/(len(final_stripped_list[i])+len(final_stripped_list[j])))
			G.add_edge(final_stripped_list[i],final_stripped_list[j], weight=cosine_similarity/(len(final_stripped_list[i])+len(final_stripped_list[j])))
			cosine_similarity=0

	#print len(G.edges())
def threshold_limit(n):
	global count
	#for (u,v,d) in G.edges(data=True):
	#	if d['weight']<=n:
	#		G.remove_edge(u,v)
	for i in range(0,len(G.edges())):
		degree_node.append(0)

	
						
	#print len(G.edges())
def Textrank_algorithm(n):
	global count
	global summary_list
	count=0
	for (u,v,d) in G.edges(data=True):
		if d['weight']<=n:
			d['weight']=0
		else:
			d['weight']=1
			degree_node[count]+=1
		count+=1;
	count=0
	for (u,v,d) in G.edges(data=True):
		if d['weight']==1:
			d['weight']=d['weight']/degree_node[count]
		count+=1
	pr = nx.pagerank_numpy(G, alpha=0.9)
	summary_list=sorted(pr.items(),key=operator.itemgetter(1),reverse=True)
	#print summary_list
	
def summary_formation():
	global summary_list
	global final_summary
	for i in range(0,len(summary_list)):
		
			final_summary=final_summary+''.join(summary_list[i][0])
			if len(final_summary.split())>=250:

				return 0
def evaluation_metrics(topic_name):
	reference=''
	global final_summary
	address=os.getcwd()+'/GroundTruth/'+topic_name+'.1'
	file_open=open(address,'r')
	for line in file_open:
		reference=reference+''.join(line)
	hypothesis=final_summary
	rouge1 = rouge.Rouge()
	scores = rouge1.get_scores(reference, hypothesis)
	print scores
topic_name=raw_input("Enter topic name")
threshold=float(raw_input("Enter the threshold"))	
t1=time.time()			
graph_construction(topic_name)
t2=time.time()
#print "The time taken for graph construction is:-",t2-t1
t1=time.time()	
tf_idf(topic_name)
t2=time.time()
#print "The time taken for tf-idf vector and cosine similarity is:-",t2-t1
t1=time.time()	
threshold_limit(threshold)
t2=time.time()
#print "The time taken for removing edges above threshold limit is:-",t2-t1
t1=time.time()	
c=Textrank_algorithm(threshold)
t2=time.time()
#print "The time taken for applying textrank algorithm is:-",t2-t1
t1=time.time()	
c=summary_formation()
t2=time.time()
#print "The time taken for summary_formation is:-",t2-t1
print "The summary is as follows:-"
print "                           "
print final_summary
print "The Evaluation metrics are as follows:-"
print "                           "
evaluation_metrics(topic_name)
