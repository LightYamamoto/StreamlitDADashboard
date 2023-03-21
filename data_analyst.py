# http://192.168.102.15:8501/
import streamlit as st
# pip install watchdogpip install watchdog
import plotly.express as px
import pandas as pd
from PIL import Image
from numerize.numerize import numerize
import streamlit.config as cfg
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# streamlit run data_analyst.py
# Setting page config
st.set_page_config(layout ='wide',initial_sidebar_state = 'expanded', page_icon = 'CellphoneS-Logo-PNG-2.png' )

# Data
def read_target_df():
# Load the target table to dataframe
    target_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEEne8cFoBE7fjE3oGhatlzaHe6cVup1lX-nfhchw4aVNRNocPaTJtZdy9aEMQ0lRFGUJmOdjGTUIU/pubhtml"
    # Clean the dataframe, remove error in unicode text and remove index column
    target_df = pd.read_html(target_url, encoding='utf-8', header = 1)[0]
    target_df = target_df.drop(columns=['1'])
    return target_df

def read_revenue_df():
    revenue_df = pd.read_excel("test.xlsx",sheet_name = "DATA 2 - DOANH SỐ BÁN" )

    return revenue_df

def join_two_df():
    target_df = read_target_df()
    revenue_df = read_revenue_df()
    df = pd.merge(target_df,revenue_df,how = 'inner',left_on='Ngành hàng', right_on='Danh mục')
    df1=df.drop(columns = 'Danh mục')
    return df1

def transformed_join_df():
    df1 = join_two_df()
    df2 = df1.copy()
    # Tạo cột Month bằng 2020-04
    df2['Month'] = '04'
    # Gán lại các giá trị Target và thực tế của tháng 4 ngược lại vào df 
    df2['Target Revenue'] = df2['2020.06']
    df2['Actual Revenue'] = df2['Doanh số tháng 4']

    df3 = df1.copy()
    df3['Month'] = '05'
    df3['Target Revenue'] = df3['2020.05']
    df3['Actual Revenue'] = df3['Doanh số tháng 5']

    df4 = df1.copy()
    df4['Month'] = '06'
    df4['Target Revenue'] = df4['2020.06']
    df4['Actual Revenue'] = df4['Doanh số tháng 6']

    df5 = pd.concat([df2,df3,df4], ignore_index=True)
    df6 = df5.drop(columns = ['2020.06','2020.05','2020.04','Doanh số tháng 6','Doanh số tháng 5','Doanh số tháng 4'])

    return df6

def read_inventory_df():
    inventory_df = pd.read_excel("test.xlsx",sheet_name = "DATA 1 - TỒN KHO THÁNG 7")
    return inventory_df

def header():
    # Create the Streamlit app layout
    header_left,header_right = st.columns([0.6, 0.4], gap ='small')
    with header_left:
        image = Image.open('cellphones_logo.png')
        st.image(image,width=200)
        # Set the vertical alignment of the header to 'center'
        # st.markdown("""
        #             <style>
        #                 /* Select the h1 element within the .css-17eq0hr class */
        #                 .css-17eq0hr h1 {
        #                     display: flex;
        #                     justify-content: right;
        #                     align-items: right;
        #                     height: 80px;
        #                     margin: 0;
        #                 }
        #             </style>
        #             """, unsafe_allow_html=True)        
    header_right.write(" Name: NGUYỄN NHẬT NGUYÊN ")
    header_right.write(" Apply Position: Data Analyst/ Data Engineer")
    header_right.write("Email: nhatnguyen1011997@gmail.com")
    header_right.write(" Phone number: 0348 468 378")
    # Set title in the Middle
    st.markdown("""
                <style>
                    .centered {
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)
    st.markdown("<h1> CellphoneS Data Analyst Test </h1>", unsafe_allow_html=True)



        
        
def row_total():        
    # Row B 
    df6 = transformed_join_df()
    total1,total2,total3,total4,total5  = st.columns(5, gap = "large")



    with total1 :
        st.image("actual.png")
        total_revenue = float(df6['Actual Revenue'].sum())
        st.metric(label = "Total Actual Revenue", value = numerize(total_revenue))

    with total3 :
        st.image("target.png")
        total_target = float(df6['Target Revenue'].sum())
        st.metric(label = "Total Target Revenue", value = numerize(total_target))
               
               
def sidebar():
    with st.sidebar:
        df6 = transformed_join_df()
        category_filter = st.multiselect(label = "Select the Category", options =df6['Ngành hàng'].unique(), default =df6['Ngành hàng'].unique() )        
        
        month_filter = st.multiselect(label = "Select the Month", options =df6['Month'].unique(), default =df6['Month'].unique() )        

    df6 = df6.rename(columns={'Ngành hàng': 'category',"Month":"month"})
    df7 = df6.query('category ==@category_filter & month == @month_filter')
    total_target  = float(df7['Target Revenue'].sum())
    total_actual  = float(df7['Actual Revenue'].sum())
    
    total1,total2,total3,total4,total5  = st.columns(5, gap = "large")
    
    with total1 :
        st.image("actual.png")
        st.metric(label = "Total Actual Revenue", value = numerize(total_actual))

    with total3 :
        st.image("target.png")
        st.metric(label = "Total Target Revenue", value = numerize(total_target))
 
    cfg.set_option('theme.sidebarWidth', 150)
  

    
def answer_1():
    st.markdown("<h3>Câu 1: Đánh giá mức độ đạt target doanh số theo ngành hàng và theo quản lí ngành hàng trong 3 tháng (4,5,6)</h3>", unsafe_allow_html= True)

    ## 2. Load data from multiple sources to DataFrame 
    st.markdown("<h4> 1. Load dữ liệu từ nhiều nguồn vào Dataframe </h4>", unsafe_allow_html=True)
    # Row A

    st.markdown("<h4>Tổng doanh thu thực tế tháng 4,5,6 </h4>", unsafe_allow_html=True)
    revenue_df = read_revenue_df()
    st.write(revenue_df)
    # st.write("")
    st.markdown("<h4>Bảng doanh thu mục tiêu theo ngành hàng và quản lí phụ trách</h4>", unsafe_allow_html=True)
    target_df = read_target_df()
    st.write(target_df)
   
    # Describle the dataset
    st.markdown("<h4> 2. Mô tả các chỉ số thống kê cơ bản của 2 tập dữ liệu </h4>", unsafe_allow_html=True)
    a1,a2  = st.columns(2, gap = 'small')
    with a1:
        st.markdown("<h5>Mô tả dữ liệu: Tổng doanh thu thực tế  </h5>", unsafe_allow_html=True)
        st.write(revenue_df.describe())
    with a2:
        st.markdown("<h5>Mô tả dữ liệu: Tổng doanh thu theo kế hoạch </h5>", unsafe_allow_html=True)
        st.write(target_df.describe())
    
    #Clean the missing data 
    st.markdown("<h4> 3.Xử lí dữ liệu bị thiếu (Deal with missing values) </h4>", unsafe_allow_html=True)
    b1,b2  = st.columns(2, gap = 'small')
    with b1:
        st.markdown("<h5>Tổng doanh thu thực tế  </h5>", unsafe_allow_html=True)
        st.write(revenue_df.isnull().sum().rename('Null Count'))
    with b2:
        st.markdown("<h5>Tổng doanh thu theo kế hoạch  </h5>", unsafe_allow_html=True)
        st.write(target_df.isnull().sum().rename('Null Count'))
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )

    st.write("Như ta đã thấy, trên bảng doanh thu thực tế theo ngành hàng của các tháng 4,5,6 không có dữ liệu bị bỏ trống, vậy nên ta có thể bỏ qua bước này. ")
    
    # Check data type
    st.markdown("<h4> 4.Check kiểu dữ liệu (Data Type) </h4>", unsafe_allow_html=True)
    c1,c2  = st.columns(2, gap = 'small')
    with c1:
        st.markdown("<h5>Tổng doanh thu thực tế  </h5>", unsafe_allow_html=True)
        st.write(revenue_df.dtypes.rename("Data Type"))
    with c2:
        st.markdown("<h5>Tổng doanh thu theo kế hoạch  </h5>", unsafe_allow_html=True)
        st.write(target_df.dtypes.rename("Data Type"))
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Tuy kiểu dữ liệu ở bảng Target đang ở dạng số nguyên (Integer) khác với kiểu dữ liệu số thực (Float) thường dùng cho tính toán doanh thu. Nhưng chúng ta cũng không cần chỉnh sửa ở kiểu dữ liệu này cho đồng bộ vì ở bước tính toán, các kiểu dữ liệu trên vẫn sẽ hiện thị đúng với mục đích phân tích. ")
    
    
    #4.(Join 2 Table) Kết hợp 2 bảng để lấy tất cả dữ liệu về cả target và cả số liệu kinh doanh thực tế của cả 3 tháng (4,5,6) 
    st.markdown("<h4> 4.(Join 2 Table) Kết hợp 2 bảng để lấy tất cả dữ liệu về cả target và cả số liệu kinh doanh thực tế của cả 3 tháng (4,5,6) </h4>", unsafe_allow_html=True)
    st.markdown("<h5>Bảng kết hợp doanh thu thực tế và doanh thu theo kế hoạch  </h5>", unsafe_allow_html=True)
    df1 = join_two_df()
    st.write(df1)
    d1,d2  = st.columns([0.7,0.3], gap = 'medium')
    with d1:
        st.write(df1.describe())
    with d2:
        st.write(df1.dtypes.rename("Data Type"))

    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    
    st.markdown("<h6>Ta có thể thấy, từ bảng kết hợp ở trên ta thấy các cột được Join khớp với nhau thông qua cột tên ngành hàng. Tuy nhiên tên các cột còn chưa đồng nhất, các thông tin trên bảng cũng khó hiểu và khó phân tích vì không biết giá trị nào là target giá trị nào là thực tế.  </h6>", unsafe_allow_html= True )
    st.markdown("<h6> Vì vậy, ta quyết định thay đổi cấu trúc của bảng dữ liệu trên cho dễ đọc hơn. Cụ thể ta thêm cột Month để thể hiện tháng được ghi nhận doanh thu. Thêm cột Target Revenue và Actual Revenue sẽ lưu các giá trị doanh thu thực tế vào mục tiêu  </h6>", unsafe_allow_html= True )
    
    # Re-Define the joined table
    st.markdown("<h4> 5. Thay đổi cấu trúc của bảng ở trên để phù hợp với bước phân tích </h4>", unsafe_allow_html=True)
    df6 =  transformed_join_df()
    st.write(df6)
    st.write(df6.shape)
    
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Ta thấy bảng trên đã gọn gàng hơn so với bảng trước đó, các thông tin được thể hiện cực kì rõ ràng, tháng và năm ghi nhận doanh thu nằm ở cột riêng, doanh thu thực tế và doanh thu ước tính được tách ra làm 2 cột dễ nhìn và dễ đọc")
    
    
def answer_2():
    st.write("Ta thấy bảng trên đã gọn gàng hơn so với bảng trước đó, các thông tin được thể hiện cực kì rõ ràng, tháng và năm ghi nhận doanh thu nằm ở cột riêng, doanh thu thực tế và doanh thu ước tính được tách ra làm 2 cột dễ nhìn và dễ đọc")
    df6 = transformed_join_df()
    st.write(df6)
    
    # Visualize the data
    st.markdown("<h5>6. Bar Chart: Mối quan hệ giữa doanh thu thực tế và doanh thu ước tính theo các ngành hàng và nhân viên quản lí ngành hàng </h5>", unsafe_allow_html= True )

    # Insert dòng Total vào Interactive Dashboard
    row_total()

    # Create a Plotly figure
    fig1 = px.bar(df6, x='Month', y=['Target Revenue', 'Actual Revenue'], barmode='group',color_discrete_sequence=['gray', 'orangered'])
    fig1.update_layout(title='Tương quan chung giữa doanh số mục tiêu và thực tế theo ngành hàng',
                    xaxis_tickangle=0,
                    xaxis_tickformat='%b',
                    height=600)
    fig1.update_xaxes(title='Month')
    fig1.update_yaxes(title='Revenue')
    st.plotly_chart(fig1)

    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Ở trên là bảng thể hiện tương quan chung về doanh thu theo kế hoạch và doanh thu thực tế của ngành hàng đồ cũ của quý công ty trong 3 tháng 4,5,6 năm 2020. ")
    st.write(" Ở tháng 4, hầu như có sự đồng nhất giữa mục tiêu đề ra và doanh số thực tế. Qua tháng 5-2020, doanh số mục tiêu được đẩy cao hơn so với mục tiêu tháng trước đó (hơn gần 4 tỷ VND doanh thu ), có thể điều này khiến cho kết quả doanh thu tháng đó bị giảm nặng, nếu có thêm số liệu, chúng ta sẽ cùng nhau phân tích thêm liệu gánh nặng KPI có ảnh hưởng xấu đến doanh số bán ra của nhân viên hay không? Hiện giờ vì không đủ dữ kiện nên ta chỉ xem đây là một giả thuyết cho những phân tích sau này ")
    st.write("Ở tháng 6, ta thấy có sự điều chỉnh lại target về lại mốc ban đầu (gần 33.4 tỷ VND). Có thể thấy được một điểm tích cực, khi điều chỉnh lại trở lại, doanh thu tháng đó lại vượt hơn KPI ~ 1.3 tỷ. Vậy nên có thể nhận định rằng, có mối quan hệ rất rõ ràng giữa target đặt ra và doanh số thực tế của nhân viên tháng đó ")

    # Xem xét mối quan hệ doanh thu so với ngành hàng
    # facet_col='Ngành hàng'
    st.markdown("<h5>7. Quan hệ doanh thu so với ngành hàng </h5>", unsafe_allow_html= True )
    fig2 = px.bar(df6, x='Ngành hàng', y=['Target Revenue', 'Actual Revenue'], barmode='group',color_discrete_sequence=['gray', 'orangered'])
    fig2.update_layout(title='Tương quan chung giữa doanh số mục tiêu và thực tế theo ngành hàng ',
                        xaxis_tickangle=45,
                        xaxis_tickformat='%b',
                        height=600)
    fig2.update_xaxes(title='Ngành Hàng')
    fig2.update_yaxes(title='Revenue')
    st.plotly_chart(fig2)
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Ở trên là bảng thể hiện tương quan của doanh thu theo ngành hàng trong 3 tháng 4,5,6 năm 2020. ")
    st.write("Ta dễ dàng nhìn thấy, ngành Iphone cũ là một ngành nổi bật vượt trội so với các ngành hàng đồ cũ còn lại. Với doanh số hơn 100 tỷ VND trong 3 tháng, ngành Iphone cũ hơn ngành Samsung cũ đang xếp thứ 2 là hơn 100 tỷ VND. Xếp thứ 3 vẫn là ngành hàng mang thương hiệu Apple(Ipad cũ). Còn tất cả các ngành hàng còn lại hầu như chiếm không đáng kể. Có thể nhận thấy, thương hiệu Apple được người dùng chấp nhận mua cũ khá nhiều, doanh thu đem lại cũng rất lớn, có thể xem xét đây là một ngành hàng lợi thế, cần đẩy mạnh đầu tư, nghiên cứu các chiến lượt PR Marketing, các đợt khuyến mãi, chế độ hậu mãi, bảo hành,.. để tối ưu ngành hàng tiềm năng này thay vì dàn trải ra nhiều ngành khác không mấy khả quan")

    
    # Xem xét mối quan hệ doanh thu so với ngành hàng
    # facet_col='Ngành hàng'
    st.markdown("<h5>7.Quan hệ doanh thu so với PIC </h5>", unsafe_allow_html= True )
    fig3 = px.bar(df6, x='PIC', y=['Target Revenue', 'Actual Revenue'], barmode='group',color_discrete_sequence=['gray', 'orangered'])
    fig3.update_layout(title='Tương quan chung giữa doanh số mục tiêu và thực tế theo PIC',
                        xaxis_tickangle=45,
                        xaxis_tickformat='%b',
                        height=600)
    fig3.update_xaxes(title='PIC')
    fig3.update_yaxes(title='Revenue')
    st.plotly_chart(fig3)
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Doanh thu theo quản lí phụ trách ngành hàng cũng có quá nhiều sự chênh lệch. Nam là bạn có doanh số bán hàng cao nhất với hơn 100 tỷ VND trong 3 tháng. Tuy vẫn còn ít hơn target đặt ra nhưng như đã phân tích ở trên, target của tháng 5 bị up lên khá nặng nên có thể coi Nam là bạn đã hoàn thành xuất sắc target đề ra. Còn 3 bạn còn lại, vì quản lí những ngành hàng khó bán ra hơn nên doanh số bán ra cũng ít hơn hẳn so với bạn đứng đầu. Ta thấy được quan hệ khá mật thiết giữa doanh số, ngành hàng và các bạn quản lí ngành hàng. Trong trường hợp này, có nhiều hướng để chứng mình xem thực sự ngành hàng ảnh hưởng tiên quyết tới doanh thu hay kĩ năng bán hàng của PIC cũng có ảnh hưởng không ít. Nếu đầy đủ dữ liệu, ta sẽ đi sâu vào phân tích mức độ tương quan giữa 3 yếu tố này. Từ đó có thể đưa ra quyết định đúng đắn để tối ưu doanh số, có thể thay đổi các bạn PIC rồi quan sát doanh thu của những tháng tới,... để xem liệu có yếu tố khách quan nào khác tác động tới doanh số bán ra không ")

def answer_3():
    st.markdown("<h3>Câu 2: Biết data tại thời điểm ngày 12/7. Đưa ra nhận xét về tồn kho theo sản phẩm, nhóm ngành hàng. Dự đoán đến cuối tháng 7, có cần thực hiện hành động  gì để đảm bảo cân đối  lượng trữ tồn hay không. Nếu có, cho ví dụ.</h3>", unsafe_allow_html= True)

    ## 2. Load data from multiple sources to DataFrame 
    st.markdown("<h4> 1. Load dữ liệu kinh doanh tháng 7 vào Dataframe </h4>", unsafe_allow_html=True)

    st.markdown("<h4>Chi tiết doanh thu thực tế 7 </h4>", unsafe_allow_html=True)
    inventory_df = read_inventory_df()
    st.write(inventory_df)
    st.write("")
    
    # Describle the dataset
    st.markdown("<h4> 2. Mô tả các chỉ số thống kê cơ bản của tập dữ liệu </h4>", unsafe_allow_html=True)
    a1,a2,a3  = st.columns(3, gap = 'large')
    with a1:
        st.markdown("<h5> Các chỉ số thống kê cơ bản </h5>", unsafe_allow_html=True)
        st.write(inventory_df.describe())
    with a2:
        st.markdown("<h5> Kiểu datatypes của bảng dữ liệu </h5>", unsafe_allow_html=True)
        st.write(inventory_df.dtypes)
    with a3:
        st.markdown("<h5> Kiểm tra giá trị bị thiếu  </h5>", unsafe_allow_html=True)
        st.write(inventory_df.isnull().sum().rename('Null Count'))       
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )

    st.write("Từ những bảng thống kê trên, ta thấy dữ liệu bị thiếu ở bảng trên khá nhiều, đối với số lượng bán và nhập theo ngày, có thể hiệu ngày đó không nhập hoặc bán sản phẩm trên. Đối với số hàng tồn có thể bán, nếu không có giá trị, ta sẽ ngầm hiểu là không có hàng tồn. Ta sẽ đi sâu vào sử lí dữ liệu bị thiếu ")
    
    
    #Clean the missing data 
    st.markdown("<h4> 3.Xử lí dữ liệu bị thiếu (Deal with missing values) </h4>", unsafe_allow_html=True)
    st.write("Đối với những dữ liệu bị thiếu trên, ta sẽ thay thế giá trị giá sản phẩm bằng giá trị trung bình của cùng ngành hàng. Ta thay số lượng bán và nhập theo ngày bằng 0 nghĩa là những ngày đó không bán hoặc nhập bất kì sản phẩm nào. Ta thay giá trị Null ở cột có thể bán bằng 0, nghĩa là không có hàng tồn. ")

    fill_values = {'Tồn có thể bán':0, 'Giá bán':0,'Số bán hôm qua':0 ,'Số bán hôm qua':0 ,'Số bán 3 ngày qua':0, 'Số bán 7 ngày qua':0,'Số nhập hôm qua':0,'Số nhập 7 ngày qua':0 }
    inventory_df.fillna(fill_values, inplace =True)

    # Tính giá trung bình cho từng nhóm sản phẩm
    mean_prices = inventory_df.groupby('Danh mục')['Giá bán'].mean()
    # Thêm giá trung bình vào cột Giá bán và điền fill_value vào các giá trị trống
    inventory_df['Giá bán'] = inventory_df['Giá bán'].fillna(inventory_df['Danh mục'].map(mean_prices))
    
    st.markdown("<h5> Sau khi đã làm sạch tập dữ liệu </h5>", unsafe_allow_html=True)
    st.write(inventory_df)
    st.write(inventory_df.isnull().sum().rename('Null Count'))
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Sau khi đã làm sạch dự liệu, ta chú ý tới vấn đề là tên Danh mục bị sai so với tên sản phẩm ")
    
    # inventory_df = inventory_df.rename(columns={'Tên sản phẩm': 'product', 'Danh mục': 'category'})
    def fix_product_name(row):
        category = row['Danh mục'].title()
        product = row['Tên sản phẩm'].title()
        if category.split()[0].lower() not in product.lower():
            return row['Danh mục'].replace(row['Tên sản phẩm'], row['Danh mục'] + ' ' + row['Tên sản phẩm'])
        else:
            return row['Tên sản phẩm']


    inventory_df['Tên sản phẩm'] = inventory_df.apply(fix_product_name, axis=1)
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Ta sẽ chỉnh sửa các tên Danh mục không trùng với tên sản phẩm như sau. Đầu tiên ta so sánh chữ cái đầu của tên danh mục xem có trùng với những chữ cái có trong tên sản phẩm hay không. Nếu trùng thì đúng, nếu không trùng thì ta sẽ thay tên danh mục thành tên sản phẩm cộng chữ Cũ")
    st.write("Sau khi thực hiện xong, ta có tập data đã làm sạch ở bên dưới")
    st.markdown("<h5> Doanh số bán hàng thực tế tháng 7 (Đã làm sạch) </h5>", unsafe_allow_html=True)
    st.write(inventory_df)


    
    #  Vẽ chart Tương quan chung giữa số hàng tồn kho theo danh mục 
    fig4 = px.bar(inventory_df, x='Danh mục', y=['Tồn có thể bán', 'Số bán 7 ngày qua'], barmode='group',color_discrete_sequence=['gray', 'orangered'])
    fig4.update_layout(title='Tương quan chung giữa số hàng tồn kho theo danh mục',
                        xaxis_tickangle=45,
                        xaxis_tickformat='%b',
                        height=800,width = 1000)
    fig4.update_xaxes(title='Tên sản phẩm')
    fig4.update_yaxes(title='Tồn kho')
    st.plotly_chart(fig4)
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("Hiện tại là ngày 12/7 và doanh số bán được trong 7 ngày qua có rất nhiều sự khác biệt đáng kể. Đối với danh mục Iphone cũ có số lượng hàng tồn nhiều nhất (lên tới hơn 2600 số lượng tồn),  trong tuần qua số lượng bán được hơn 800 sản phẩm, chỉ mới giải quyết được hơn 1/3 so với số lượng tồn kho hiện tại. Đối với Samsung cũ, tuy số lượng bán ra không nhiều bằng Iphone nhưng trong một tuần qua, lượng bán ra đã gần bằng con số nhập vào cho tới thời điểm hiện tại. Ipad cũ, Apple Watch cũ vẫn đang ghi nhận số lượng bán ra trung bình. Riêng VSMart cũ có số lượng cầu vượt cung, tuy nhiên số lượng bán ra vẫn không đáng kể ")
    st.write("Để hiểu rõ hơn về doanh số các sản phẩm được bán ra trong tuần qua, ta hãy xem bảng bên dưới")
    
    
    #  Vẽ chart Tương quan chung giữa số hàng tồn kho theo danh mục sản phẩm
    st.markdown("<h5> 4.Biết data tại thời điểm ngày 12/7. Đưa ra nhận xét về tồn kho theo sản phẩm, nhóm ngành hàng. </h5>", unsafe_allow_html=True)
    fig5 = px.bar(inventory_df, x='Tên sản phẩm', y=['Tồn có thể bán', 'Số bán 7 ngày qua'], barmode='group',color_discrete_sequence=['gray', 'orangered'])
    fig5.update_layout(title='Tương quan chung giữa số hàng tồn kho theo tên sản phẩm',
                        xaxis_tickangle=45,
                        xaxis_tickformat='%b',
                        height=800,width = 1000)
    fig5.update_xaxes(title='Tên sản phẩm')
    fig5.update_yaxes(title='Tồn kho')
    st.plotly_chart(fig5)
    
    # Comment on an issue
    st.markdown("<h5>Comment: </h5>", unsafe_allow_html= True )
    st.write("")
    st.write("Từ bảng này, ta có thể nhận thấy rằng các sản phẩm của nhà Apple đang chiếm ưu thế về doanh số bán ra, với sản phẩm Iphone XSMax 64Gb cũ dẫn đầu với hơn 100 sản phẩm bán ra trong tuần. Các sản phẩm khác như Iphone 8 64Gb, Iphone XSMax 256Gb,.. cũng đứng đầu trong số lượng bán ra. Điều đáng chú ý là gần như 90% số lượng sản phẩm bán ra là các sản phẩm điện thoại Iphone. Điều này cho thấy sự ưa chuộng của khách hàng đối với các sản phẩm của Apple. Có thể do Apple đang có chiến lược kinh doanh hiệu quả với các sản phẩm điện thoại của mình, tạo ra được sự tin tưởng và đánh giá cao từ người tiêu dùng. Ngoài ra, cũng có thể là do các sản phẩm điện thoại Iphone có thiết kế đẹp, tính năng ấn tượng, và được nâng cấp thường xuyên, tạo ra sự hấp dẫn đối với khách hàng. Tuy nhiên, việc phân tích chỉ dựa trên bảng thống kê này có thể hạn chế, cần phải xem xét thêm các yếu tố khác như giá cả, chất lượng sản phẩm và chiến lược marketing của các thương hiệu khác để có thể đưa ra những kết luận chính xác hơn.")
    
    st.markdown("<h5>Nhận xét:Cần thực hiện hành động gì để đảm bảo cân đối lượng trữ tồn. </h5>", unsafe_allow_html= True )

    st.write("Với tình hình bán hàng như vậy, chính sách quản lí hàng tồn của doanh nghiệp nên tập trung vào việc quản lý lượng tồn kho của sản phẩm Iphone một cách hiệu quả để đảm bảo cung cấp đủ sản phẩm cho khách hàng mà không gây ra lượng hàng tồn kho quá lớn. Cụ thể, doanh nghiệp có thể áp dụng các chiến lược quản lý hàng tồn như quản lý hàng tồn kho theo phương pháp FIFO (First-In-First-Out), đó là sản phẩm được nhập vào trước sẽ được bán ra trước. Điều này giúp đảm bảo rằng sản phẩm được bán ra là những sản phẩm mới nhất và đảm bảo chất lượng sản phẩm. Ngoài ra, doanh nghiệp cũng nên sử dụng các công cụ quản lý kho và thống kê để theo dõi số lượng hàng tồn kho và số lượng bán ra của từng sản phẩm, từ đó đưa ra các quyết định hợp lý về việc nhập kho, xuất kho, hoặc giảm giá sản phẩm để đáp ứng nhu cầu của khách hàng và đảm bảo cân đối lượng trữ tồn. Ngoài ra, doanh nghiệp cũng nên xem xét đến việc đa dạng hóa sản phẩm và mở rộng thị trường để giảm thiểu rủi ro về việc phụ thuộc vào một sản phẩm duy nhất, đồng thời tăng cường quảng bá và tiếp cận khách hàng để tăng doanh số bán hàng và đảm bảo cân đối lượng tồn kho của toàn bộ sản phẩm.")
    
    st.markdown("<h5>Ví dụ: </h5>", unsafe_allow_html= True )

    st.write("Ví dụ thực tế , doanh nghiệp CellphoneS sản xuất và kinh doanh các sản phẩm điện tử như, Iphone, Samsung, Apple Watch, Xiaomi Band,.... Trong đó, sản phẩm Iphone bán ra nhiều hơn các sản phẩm khác. Do đó, doanh nghiệp cần tập trung vào việc quản lý lượng tồn kho của các sản phẩm Iphone này bằng cách thu thập số liệu một cách đầy đủ logic, tên database các cột dòng phải được chuẩn hóa kĩ, các kiểu dữ liệu phải được set hợp lí. Bằng cách có được một Database kinh doanh tốt, ta có thể dựa vào dữ liệu trong quá khứ để phân tích trend, pattern, xu hướng mua sắm và thị hiếu của khách hàng, từ đó ta có thể dễ dàng chủ động được số hàng tồn trong kho dựa trên số liệu đã được dự đoán trước. Bên cạnh đó, với các sản phẩm khó được lòng của khách hàng, ta nên đưa ra những chương trình khuyến mãi, những chính sách giảm giá để đẩy mạnh doanh số bán hàng của các sản phẩm đó, giúp cân đối lượng trữ tồn, tránh bị mất cân đối và bị phụ thuộc vào môt vài món hàng, giúp đảm bảo doanh thu cho toàn bộ sản phẩm.")

def page_1():
    header()
    answer_1()
    
def page_2():
    header()
    answer_2()
    
def page_3():
    header()

    answer_3()   
    
# Define main  to run all the functions
def main():
    # Create the sidebar navigation
    st.sidebar.title("Choose Page")
    page = st.sidebar.radio("Go to", ["Page 1: Load,Clean and Transform Dataset", "Page 2: Visualization the Data","Page 3: Answer question 2"])
    
    # Run Page 1 setting
    if page == "Page 1: Load,Clean and Transform Dataset":
        with st.container():
            page_1()
            
        st.write("")    
        st.write("")    
        st.markdown("<h5>End of page 1</h5>",unsafe_allow_html=True)
    
    # Run Page 2 setting
    elif page == "Page 2: Visualization the Data":
        with st.container():
            page_2()
            st.write("This is page 2")
            
    # Run Page 1 setting
    elif page == "Page 3: Answer question 2":
        with st.container():
            page_3()
            
            st.markdown("<h3>End of Test. Thanks for reading</h3>",unsafe_allow_html=True)

            
            
if __name__ == "__main__":
    main()